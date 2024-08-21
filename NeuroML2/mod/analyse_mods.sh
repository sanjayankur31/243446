# BK_Slow.mod  capmax.mod  CaP.mod  CaT.mod  cdp_AIS.mod  cdp_smooth.mod  cdp_soma.mod  cdp_spiny.mod  distr.mod  ih.mod
# Kv1.mod  kv3.mod  kv4f.mod  kv4s.mod  mslo.mod  nap.mod  narsg.mod  peak.mod  pkjlk.mod  SK2.mod  syn2.mod
#
echo "Compiling mod files"
nrnivmodl .

parallel_run() {
    parallel -j $1 --\
        "pynml-modchananalysis BK_Slow -duration 100000"\
        "pynml-modchananalysis CaP"\
        "pynml-modchananalysis CaT"\
        "pynml-modchananalysis ih -duration 50000"\
        "pynml-modchananalysis Kv1 -duration 150000"\
        "pynml-modchananalysis kv3"\
        "pynml-modchananalysis kv4f"\
        "pynml-modchananalysis kv4s -duration 100000"\
        "pynml-modchananalysis mslo"\
        "pynml-modchananalysis nap"\
        "pynml-modchananalysis narsg -duration 100000"\
        "pynml-modchananalysis SK2"

}

serial_run () {
    pynml-modchananalysis BK_Slow -duration 100000
    pynml-modchananalysis CaP
    pynml-modchananalysis CaT
    pynml-modchananalysis ih -duration 50000
    pynml-modchananalysis Kv1 -duration 150000
    pynml-modchananalysis kv3
    pynml-modchananalysis kv4f
    pynml-modchananalysis kv4s -duration 100000
    pynml-modchananalysis mslo
    pynml-modchananalysis nap
    pynml-modchananalysis narsg -duration 100000
    pynml-modchananalysis SK2
}

echo "Analysing mod files"

serial_run

## if gnu parallel is available, use the parallel run, argument is number of parallel jobs:
# parallel_run 6
