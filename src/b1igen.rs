use num_complex::Complex32;

use crate::satellite_loader::Bds2SatelliteInfo;

pub struct B1iSimulation {
    satellites: Vec<Bds2SatelliteInfo>,
    sim_time: f64,
    sim_step: f64,
    
}