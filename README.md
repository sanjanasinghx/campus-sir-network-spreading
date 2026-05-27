# SIR Epidemic Simulation on a Campus Contact Network

Zone-level SIR model on a weighted 9-node campus contact graph. I compare two seed locations, a well-mixed baseline, and a hostel-isolation intervention.

Coursework for ES 404 Networks and Complex Systems, IIT Gandhinagar, 2026. [Report (PDF)](./report.pdf) | [Academia.edu](https://telaviv.academia.edu/SanjanaSingh)

2,530 people are split across nine zones (three hostel clusters, dining hall, library, academic core, labs, sports area, main gate), connected by 14 weighted undirected edges for contact intensity. Each zone's force of infection mixes local prevalence with an import term from neighbouring zones through the row-normalised adjacency matrix.

Four runs:

1. Scenario A: outbreak seeded in Hostel 2 (H2), a hostel zone away from the hub.
2. Scenario B: outbreak seeded in the academic core (A), the highest-degree hub.
3. Well-mixed baseline: homogeneous SIR with the same beta, mu, N and I(0).
4. Intervention: H2 isolated from day 7 (edge weights cut by 80%).

## Results

- R0 = 1.70 (beta/mu = 0.34/0.20). With only 5 of 2,530 people infected at the start, the outbreak takes a while to build up.
- Seeding at the hub matters: Scenario B peaks about 45 infections higher than Scenario A and has 163 more cumulative infections by day 30 (609 vs 446).
- The network model with a hub seed peaks about 11% higher than the well-mixed baseline. The well-mixed model underestimates early spread.
- Isolating H2 cuts the peak by 16.6% and cumulative cases by 17% by day 30. It mostly flattens the peak rather than preventing the outbreak.
- Peripheral zones (Sports, Gate) stay fairly protected wherever the outbreak is seeded.

## Tools

numpy, `scipy.integrate.solve_ivp` (RK45), networkx, matplotlib

## Running it

```bash
git clone https://github.com/sanjanasinghx/campus-sir-network-spreading.git
cd campus-sir-network-spreading
pip install -r requirements.txt

# Run simulations (writes .npz to data/)
python src/simulate.py

# Make figures (writes PDFs to figures/)
python plotting/plotting.py
```

Simulation outputs are already in `data/` and figures in `figures/`, so you don't need to re-run anything to look at them.

## Layout

```
src/
  network.py          campus graph: 9 zones, weighted edges, centrality measures
  simulate.py         runs all 4 scenarios
  sir_network.py      zone-level SIR ODE
  sir_wellmixed.py    well-mixed SIR baseline
  style.py            matplotlib style and colours
plotting/
  plotting.py         makes the 7 figures
figures/              PDF figures
data/                 .npz simulation outputs
report.pdf            written report
requirements.txt
```

## Related repos

- [`rsfmri-connectivity-cpm`](https://github.com/sanjanasinghx/rsfmri-connectivity-cpm): resting-state fMRI connectivity and predictive modelling
- [`eeg-erp-auditory-oddball`](https://github.com/sanjanasinghx/eeg-erp-auditory-oddball): single-subject EEG/ERP pipeline in MNE-Python
- [`infant-eeg-spectral-fooof`](https://github.com/sanjanasinghx/infant-eeg-spectral-fooof): developmental EEG spectral and aperiodic analysis

## References

- Kermack, W.O. & McKendrick, A.G. (1927). A contribution to the mathematical theory of epidemics. *Proc. R. Soc. Lond. A*, 115(772), 700-721.
- Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.

## License

Code: MIT. Report text: CC BY 4.0.
