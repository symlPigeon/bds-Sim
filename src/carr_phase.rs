use num_complex::Complex32;

use crate::constants::LIGHT_SPEED;

/// 计算得到载波相位（0-2pi）
pub fn get_carr_phase(delay: f64, freq: f64) -> f64 {
    let dist = LIGHT_SPEED * delay;
    let lambda = LIGHT_SPEED / freq;
    
    2.0 * std::f64::consts::PI * ((dist / lambda) % 1.0)
}

/// 计算由于运动导致的伪距变化引发的相位变化幅度
pub fn get_carr_phase_shift(delay: f64, prev_delay: f64, freq: f64, interval: f64) -> f64 {
    let dist = LIGHT_SPEED * delay;
    let prev_dist = LIGHT_SPEED * prev_delay;
    let lambda = LIGHT_SPEED / freq;
    let phase = 2.0 * std::f64::consts::PI * ((dist / lambda) % 1.0);
    let prev_phase = 2.0 * std::f64::consts::PI * ((prev_dist / lambda) % 1.0);
    
    (phase - prev_phase) / interval
}

/// 从载波相位得到复32位采样
pub fn complex32_from_phase(phase: f64) -> Complex32 {
    Complex32::new(phase.cos() as f32, phase.sin() as f32)
}
