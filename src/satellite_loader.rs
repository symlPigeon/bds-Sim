pub trait SatelliteLoader {
    fn get_prn_bit(&self, idx: usize) -> u8;
    fn get_elevation(&self, idx: usize) -> f64;
    fn get_delay(&self, idx: usize) -> f64;
    fn get_data_bit(&self, idx: usize) -> u8;
    fn ref_delay(&self) -> f64;
    fn sample_length(&self) -> usize;
}

pub struct Bds2SatelliteInfo {
    pub prn: Vec<u8>,
    pub elevation: Vec<f64>,
    pub delay: Vec<f64>,
    pub ref_delay: f64,
    pub data: Vec<u8>,
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
                .map(|d| d as u8) // split to bits
                .flat_map(|d| (0..4).map(move |i| (d >> i) & 1).rev())
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
                .map(|d| d as u8)
                .flat_map(|d| (0..3).map(move |i| (d >> i) & 1).rev())
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
        
        assert!(elevation.len() == delay.len());

        Ok(Bds2SatelliteInfo {
            prn,
            elevation,
            delay,
            ref_delay,
            data,
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
    fn get_data_bit(&self, idx: usize) -> u8 {
        self.data[idx % self.data.len()]
    }
    fn get_delay(&self, idx: usize) -> f64 {
        self.delay[idx % self.delay.len()]
    }
    fn get_elevation(&self, idx: usize) -> f64 {
        self.elevation[idx % self.elevation.len()]
    }
    fn get_prn_bit(&self, idx: usize) -> u8 {
        self.prn[idx % self.prn.len()]
    }
    fn ref_delay(&self) -> f64 {
        self.ref_delay
    }
    fn sample_length(&self) -> usize {
        self.delay.len()
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
