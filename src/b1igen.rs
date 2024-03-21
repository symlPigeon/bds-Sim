use std::io::Write;

use num_complex::Complex32;

use crate::{
    carr_phase::get_carr_phase, constants::{B1I_NH_CODE, B1I_NH_LEN, B1I_PRN_LEN, BDS2_FREQ, LIGHT_SPEED}, satellite_loader::{Bds2SatelliteInfo, SatelliteLoader}
};

pub struct B1iSimulation {
    satellites: Vec<B1iSatelliteWrapper>,
    delay_step: f64,
    sim_data: Vec<Complex32>,
    sim_step: f64,
    file_handler: std::fs::File,
}

impl B1iSimulation {
    pub fn new(
        msg_path: &str,
        delay_step: f64,
        sample_rate: f64,
        output_name: &str,
    ) -> Result<B1iSimulation, String> {
        println!("[1/4] Loading satellite data...");
        let satellites = Bds2SatelliteInfo::from_file(msg_path)?
            .into_iter()
            .map(|x| B1iSatelliteWrapper::new(x, delay_step, 1.0 / sample_rate))
            .collect::<Vec<B1iSatelliteWrapper>>();
        let sim_step = 1.0 / sample_rate;
        let sim_data = Vec::new();
        let file_handler = std::fs::File::create(output_name).map_err(|e| e.to_string())?;
        Ok(B1iSimulation {
            satellites,
            delay_step,
            sim_data,
            sim_step,
            file_handler,
        })
    }

    pub fn simulate(&mut self) {
        println!("[2/4] Initializing system...");
        for satellite in self.satellites.iter_mut() {
            satellite.init();
        }
        println!("  * Satellites initialized.");
        let end_time = (self.satellites[0].satellite.sample_length() - 2) as f64 * self.delay_step;
        //                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  ^ decrease 1 to avoid overflow
        let iter_nums = (end_time / self.sim_step) as u64;
        let update_interval = (self.delay_step / self.sim_step) as usize;
        println!("Simulating for {} seconds...", end_time);
        println!("[3/4] Start simulation...");
        let bar = indicatif::ProgressBar::new(iter_nums);
        for idx in 0..iter_nums {
            // ! Parallel causes poor performance...
            // let sample: Complex32 = self.satellites.par_iter_mut().map(|s| s.simulate()).sum();

            let mut sample = Complex32::new(0.0, 0.0);
            for satellite in self.satellites.iter_mut() {
                sample += satellite.simulate();
            }

            self.sim_data.push(sample);
            bar.inc(1);
            if idx as usize % update_interval == 0 {
                for satellite in self.satellites.iter_mut() {
                    satellite.update();
                }
            }
            if idx as usize % (update_interval * 10) == 0 && idx != 0 {
                self.export();
            }
        }
        bar.finish();
        println!("[4/4] Stop simulation.");
    }

    fn export(&mut self) {
        unsafe {
            let data_ptr = self.sim_data.as_ptr() as *const u8;
            let data_len = self.sim_data.len() * std::mem::size_of::<Complex32>();
            let data = std::slice::from_raw_parts(data_ptr, data_len);
            self.file_handler.write_all(data).unwrap();
        }
        self.sim_data.clear();
        assert!(self.sim_data.is_empty());
    }
}

pub struct B1iSatelliteWrapper {
    satellite: Bds2SatelliteInfo,
    curr_time: f64,
    delay_idx: usize,
    delay: f64,
    ref_delay: f64,
    elevation: f64,
    phase_shift: f64,
    delay_step: f64,
    sim_step: f64,
    cached_phase: Complex32
}

impl B1iSatelliteWrapper {
    pub fn new(
        satellite: Bds2SatelliteInfo,
        delay_step: f64,
        sim_step: f64,
    ) -> B1iSatelliteWrapper {
        B1iSatelliteWrapper {
            satellite,
            curr_time: 0.0,
            delay_idx: 0,
            delay: 0.0,
            ref_delay: 0.0,
            elevation: 0.0,
            phase_shift: 0.0,
            delay_step,
            sim_step,
            cached_phase: Complex32::new(0.0, 0.0)
        }
    }

    fn get_idx_by_time(&self, curr_time: f64) -> (usize, usize, usize) {
        let start_time_ims = (curr_time * 1000.0) as usize; // how many ms have passed
        let start_time_ms = curr_time - start_time_ims as f64; // inside the current ms, how much time has passed
        let prn_idx = (start_time_ms * B1I_PRN_LEN as f64) as usize; // in 1ms we transmit all 2046 PRN bits
        let nh_idx = start_time_ims % B1I_NH_LEN; // one nh bit lasts 1ms, in 20ms we transmit all nh bits
        let msg_idx = start_time_ims / B1I_NH_LEN; // one message bit lasts 20ms
        (prn_idx, nh_idx, msg_idx)
    }

    fn doppler_shift(&self) -> f64 {
        // f_d = \frac{v}{c} \cdot f_0
        let delta_t = self.delay - self.ref_delay;
        let delta_dist = delta_t * LIGHT_SPEED;
        let v = delta_dist / self.delay_step;
        v / LIGHT_SPEED * BDS2_FREQ
    }

    fn init(&mut self) {
        // init parameters for simulation...
        self.curr_time = 6.0 - self.satellite.get_delay(0); // 1 message unit = 6 seconds, add this to avoid negative start time
        self.delay = self.satellite.get_delay(self.delay_idx);
        self.ref_delay = self.satellite.ref_delay();
        self.elevation = self.satellite.get_elevation(self.delay_idx);
        self.delay_idx += 1;
        // calculate phase shift
        // the movement of satellites and receiver will cause phase shift
        let freq_shift = self.doppler_shift();
        self.phase_shift = 2.0 * std::f64::consts::PI * freq_shift * self.sim_step; // in 1 sim_step, doppler shift causes phase shift of 2\pi f \Delta t
        let cached_phase = get_carr_phase(self.delay, BDS2_FREQ);
        self.cached_phase = Complex32::new(cached_phase.cos() as f32, cached_phase.sin() as f32);
    }

    fn update(&mut self) {
        self.ref_delay = self.delay;
        self.delay = self.satellite.get_delay(self.delay_idx);
        self.elevation = self.satellite.get_elevation(self.delay_idx);
        self.delay_idx += 1;
        let freq_shift = self.doppler_shift();
        self.phase_shift = 2.0 * std::f64::consts::PI * freq_shift * self.sim_step; // frequency shift causes phase shift
    }

    pub fn simulate(&mut self) -> Complex32 {
        let (prn_idx, nh_idx, msg_idx) = self.get_idx_by_time(self.curr_time);
        let prn_bit = self.satellite.get_prn_bit(prn_idx);
        let nh_bit = B1I_NH_CODE[nh_idx];
        let msg_bit = self.satellite.get_data_bit(msg_idx);
        let modulation_bit = (prn_bit ^ nh_bit ^ msg_bit) as f32 * 2.0 - 1.0; // to BPSK bits
        self.cached_phase *= modulation_bit;
        self.cached_phase += Complex32::new(self.phase_shift.cos() as f32, self.phase_shift.sin() as f32);
        self.curr_time += self.sim_step;
        self.cached_phase
    }
}
