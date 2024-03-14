use crate::constants::B1I_PRN_LEN;

pub trait SatelliteLoader {
    fn next_prn_bit(&mut self) -> u8;
    fn next_elevation(&mut self) -> f64;
    fn next_delay(&mut self) -> f64;
    fn next_data_bit(&mut self) -> u8;
    fn ref_delay(&self) -> f64;
}

pub struct Bds2SatelliteInfo {
    pub prn: Vec<u8>,
    pub elevation: Vec<f64>,
    pub delay: Vec<f64>,
    pub ref_delay: f64,
    pub data: Vec<u8>,
    prn_idx: usize,
    data_idx: usize,
    delay_idx: usize,
    elevation_idx: usize,
}

impl Bds2SatelliteInfo {
    fn new_from_json(json: serde_json::Value) -> Result<Self, String> {
        let data: Vec<u8> = match json.get("data") {
            // hex string to u8
            Some(data) => data
                .as_str()
                .ok_or("Field `data` is not a String!")?
                .chars()
                .map(|c| c.to_digit(16).ok_or("Invalid hex digit!"))
                .collect::<Result<Vec<u32>, &str>>()?
                .into_iter()
                .map(|d| {
                    // convert u32 to u8
                    d as u8
                })
                .collect(),
            None => return Err("Field `data` not found!".to_string()),
        };
        let prn: Vec<u8> = match json.get("prn") {
            Some(prn) => prn
                .as_str()
                .ok_or("Field `prn` is not a String!")?
                .chars()
                .map(|c| c.to_digit(8).ok_or("Invalid digit!"))
                .collect::<Result<Vec<u32>, &str>>()?
                .into_iter()
                .map(|d| {
                    // convert u32 to u8
                    d as u8
                })
                .collect(),
            None => return Err("Field `prn` not found!".to_string()),
        };
        let elevation: Vec<f64> = match json.get("elevation") {
            Some(elevation) => elevation
                .as_array()
                .ok_or("Field `elevation` is not an Array!")?
                .iter()
                .map(|e| e.as_f64().ok_or("Invalid elevation!"))
                .collect::<Result<Vec<f64>, &str>>()?,
            None => return Err("Field `elevation` not found!".to_string()),
        };
        let delay: Vec<f64> = match json.get("delay") {
            Some(delay) => delay
                .as_array()
                .ok_or("Field `delay` is not an Array!")?
                .iter()
                .map(|e| e.as_f64().ok_or("Invalid delay!"))
                .collect::<Result<Vec<f64>, &str>>()?,
            None => return Err("Field `delay` not found!".to_string()),
        };
        let ref_delay: f64 = match json.get("refDelay") {
            Some(ref_delay) => ref_delay
                .as_f64()
                .ok_or("Field `ref_delay` is not a Float!")?,
            None => return Err("Field `ref_delay` not found!".to_string()),
        };

        Ok(Bds2SatelliteInfo {
            prn,
            elevation,
            delay,
            ref_delay,
            data,
            prn_idx: 0,
            data_idx: 0,
            delay_idx: 0,
            elevation_idx: 0,
        })
    }

    pub fn from_file(filename: &str) -> Result<Vec<Self>, String> {
        // load data from file
        let file = std::fs::File::open(filename).map_err(|e| e.to_string())?;
        let reader = std::io::BufReader::new(file);
        let json: Vec<serde_json::Value> =
            serde_json::from_reader(reader).map_err(|e| e.to_string())?;

        let mut satellites = Vec::new();
        for element in json.iter() {
            let satellite_info = Bds2SatelliteInfo::new_from_json(element.clone())?;
            satellites.push(satellite_info);
        }
        Ok(satellites)
    }
}

impl SatelliteLoader for Bds2SatelliteInfo {
    fn next_prn_bit(&mut self) -> u8 {
        let prn_idx = self.prn_idx / 3;
        let bit_idx = self.prn_idx % 3;
        let bit = (self.prn[prn_idx] >> (2 - bit_idx)) & 1;
        self.prn_idx += 1;
        if self.prn_idx >= B1I_PRN_LEN {
            self.prn_idx = 0;
        }
        bit
    }
    fn next_data_bit(&mut self) -> u8 {
        let data_idx = self.data_idx / 4;
        let bit_idx = self.data_idx % 4;
        let bit = (self.data[data_idx] >> (3 - bit_idx)) & 1;
        self.data_idx += 1;
        if self.data_idx >= self.data.len() * 4 {
            self.data_idx = 0;
        }
        bit
    }
    fn next_delay(&mut self) -> f64 {
        let delay = self.delay[self.delay_idx];
        self.delay_idx += 1;
        if self.delay_idx >= self.delay.len() {
            self.delay_idx = 0;
        }
        delay
    }
    fn next_elevation(&mut self) -> f64 {
        let elevation = self.elevation[self.elevation_idx];
        self.elevation_idx += 1;
        if self.elevation_idx >= self.elevation.len() {
            self.elevation_idx = 0;
        }
        elevation
    }
    fn ref_delay(&self) -> f64 {
        self.ref_delay
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_from_file() {
        let filename = "msg.json";
        let satellites = Bds2SatelliteInfo::from_file(filename);

        match satellites {
            Ok(_) => {}
            Err(e) => {
                println!("{}", e);
                panic!();
            }
        }
    }
}
