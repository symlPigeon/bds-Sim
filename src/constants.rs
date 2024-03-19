pub const LIGHT_SPEED: f64 = 299792458.0;
pub const BDS2_FREQ: f64 = 1561.098e6;
pub const BDS2_LAMBDA: f64 = LIGHT_SPEED / BDS2_FREQ;

pub const B1I_PRN_LEN: usize = 2046;
pub const B1I_NH_LEN: usize = 20;
pub const B1I_NH_CODE: [u8; B1I_NH_LEN] =
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0];
