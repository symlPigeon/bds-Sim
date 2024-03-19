use bds_sim_tx::b1igen::B1iSimulation;

fn main() {
    let mut b1igen = B1iSimulation::new("msg.json", 0.1, 5e6).unwrap();
    b1igen.simulate();
    b1igen.export("out.bin");
}