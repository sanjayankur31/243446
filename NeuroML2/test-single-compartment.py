#!/usr/bin/env python3
"""
Test a single compartment cell with all biophysics

File: test-single-compartment.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""

import random
import shutil
import neuron
import datetime
import subprocess
from pyneuroml.plot import generate_plot
from pyneuroml.neuron.analysis.HHanalyse import get_states
from pyneuroml.utils.plot import get_next_hex_color
import typing
import numpy


timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def test_single_compartment_neuron_model(
    amplitude: typing.Optional[str] = None,
    ca_clamp: bool = False,
):
    """Test a single compartment NEURON model with all mechanisms

    Four phases:

    - 0 - 1500:no calcium clamp, no current
    - 1500 - 3000: with calcium clamp only
    - 3000 - 4500: with current only
    """
    myrand = random.Random(123)
    shutil.rmtree("x86_64", ignore_errors=True)

    # channel parameters to loop through
    channel_folder: str = "mod"
    channels: typing.Dict[str, typing.Dict[str, str]] = {
        "BK_Slow": {},
        "CaP": {},
        "CaT": {},
        "ih": {},
        "Kv1": {},
        "kv3": {},
        "kv4f": {},
        "kv4s": {},
        "mslo": {},
        "nap": {},
        "narsg": {},
        "SK2": {},
    }

    h = neuron.h
    h.celsius = 34
    h.load_file("stdrun.hoc")
    h(
        """
    objref p
    p = new PythonObject()
    """
    )
    # Create a section, set size & insert pas, passive channel mechanism
    soma = h.Section(name="soma")

    soma.L = 10
    soma.nseg = 1
    for seg in soma:
        soma.diam = 5
        soma.cm = 0.64
        soma.Ra = 120

    # always insert pas
    soma.insert("pas")
    soma(0.5).g_pas = 1 / 120236  # 1/ohm-cm2
    soma(0.5).e_pas = -65

    # calcium clamp
    if ca_clamp is True:
        try:
            soma.insert("CaClamp")
        except ValueError:
            try:
                subprocess.run(
                    args=["nrnivmodl", "mod"], check=True, capture_output=True
                )
            except subprocess.CalledProcessError:
                return 1

            h.nrn_load_dll("x86_64/.libs/libnrnmech.so")
            soma.insert(str("CaClamp"))
            setattr(soma(0.5), "conc0_CaClamp", 1e-5)
            setattr(soma(0.5), "conc1_CaClamp", 1e-4)
            setattr(soma(0.5), "delay_CaClamp", 2000)
            setattr(soma(0.5), "cai", 1e-4)
            setattr(soma(0.5), "cao", 2)

        ca_obj = getattr(soma(0.5), "_ref_cai")
        caRec = h.Vector().record(ca_obj)

    channel_states_rec = {}
    for channel, params in channels.items():
        states_rec = {}
        try:
            soma.insert(str(channel))
        except ValueError:
            try:
                subprocess.run(
                    args=["nrnivmodl", channel_folder], check=True, capture_output=True
                )
            except subprocess.CalledProcessError:
                return 1
            h.nrn_load_dll("x86_64/.libs/libnrnmech.so")
            soma.insert(str(channel))

        for pname, pvalue in params.items():
            setattr(soma(0.5), pname, float(pvalue))

        modFileName = f"{channel_folder}/{channel}.mod"
        with open(modFileName, "r") as handle:
            modFileTxt = handle.read()
        states = get_states(modFileTxt)

        # remove unused states
        try:
            states.remove("Ca")
        except ValueError:
            pass
        try:
            states.remove("Ia")
        except ValueError:
            pass

        states = sorted(states)
        for s in states:
            chan_obj = getattr(soma(0.5), f"_ref_{s}_{channel}")
            states_rec[s] = h.Vector().record(chan_obj)
        channel_states_rec[channel] = states_rec

    # current clamp
    if amplitude is not None:
        ic = h.IClamp(soma(0.5))
        ic.delay = 3500
        ic.dur = 500
        ic.amp = float(amplitude)

    # recordings
    vRec = h.Vector().record(soma(0.5)._ref_v)
    tRec = h.Vector().record(h._ref_t)

    # since there are two calciums in the cell (see CaT.mod)
    # ca
    ica_object = getattr(soma(0.5), "_ref_ica")
    ica = h.Vector().record(ica_object)

    # Ca: CaT
    iCa_object = getattr(soma(0.5), "_ref_iCa")
    iCa = h.Vector().record(iCa_object)

    # run
    v0 = -65.0  # Pre holding potential
    h.finitialize(v0)
    h.dt = 0.01
    h.continuerun(5000)

    # v
    generate_plot(
        xvalues=[tRec.to_python()],
        yvalues=[vRec.to_python()],
        title="NEURON",
        labels=["v"],
        show_plot_already=True,
        xaxis="time (ms)",
        yaxis="v (mV)",
        ylim=[-200, 200],
        save_figure_to=f"{timestamp}_test_{channel}_NEURON.png",
        title_above_plot="NEURON",
        legend_position="outer right",
    )

    # ca clamp
    if ca_clamp is True:
        generate_plot(
            xvalues=[tRec.to_python()],
            yvalues=[caRec.to_python()],
            title="NEURON",
            labels=["caConc"],
            show_plot_already=True,
            xaxis="time (ms)",
            yaxis="conc",
            save_figure_to=f"{timestamp}_test_{channel.lower()}_ca_NEURON.png",
            title_above_plot="NEURON",
            legend_position="outer right",
        )

    # ca
    generate_plot(
        xvalues=[tRec.to_python()],
        yvalues=[numpy.array(ica.to_python()) * 10],  # convert to SI
        title="NEURON",
        labels=["ica"],
        show_plot_already=True,
        xaxis="time (ms)",
        yaxis="i",
        save_figure_to=f"{timestamp}_test_{channel.lower()}_ca_i_NEURON.png",
        title_above_plot="NEURON",
        legend_position="outer right",
    )

    # Ca
    generate_plot(
        xvalues=[tRec.to_python()],
        yvalues=[numpy.array(iCa.to_python()) * 10],  # convert to SI
        title="NEURON",
        labels=["iCa"],
        show_plot_already=True,
        xaxis="time (ms)",
        yaxis="i",
        save_figure_to=f"{timestamp}_test_{channel.lower()}_ca_i_NEURON.png",
        title_above_plot="NEURON",
        legend_position="outer right",
    )

    # all states
    for channel, states in channel_states_rec.items():
        colors = [get_next_hex_color(myrand) for i in range(len(states))]
        generate_plot(
            xvalues=[tRec.to_python()] * len(states),
            yvalues=[rec.to_python() for rec in states.values()],
            title=f"NEURON: states ({channel})",
            labels=list(states.keys()),
            colors=colors,
            show_plot_already=True,
            xaxis="time (ms)",
            yaxis="rate",
            ylim=[-0.1, 1.1],
            save_figure_to=f"{timestamp}_test_{channel.lower()}_states_NEURON.png",
            title_above_plot="NEURON",
            legend_position="outer right",
        )

    """
    return {
        "t": tRec.to_python(),
        "states": [rec.to_python() for rec in states_rec],
        "ica": list(numpy.array(ica.to_python()) * 10),  # conver to SI
    }
    """


def test_NML_model():
    """Test a single compartment NML model with all mechanisms"""
    pass


if __name__ == "__main__":
    test_single_compartment_neuron_model(amplitude="0.001", ca_clamp=True)
