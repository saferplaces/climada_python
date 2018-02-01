"""
test plots
"""
import unittest
import numpy as np
import matplotlib.pyplot as plt

from climada.entity.entity import Entity
from climada.hazard.source_mat import HazardMat
from climada.entity.exposures.source_excel import ExposuresExcel
from climada.entity.impact_funcs.source_excel import ImpactFuncsExcel
from climada.engine.impact import Impact, ImpactFreqCurve
from climada.util.constants import HAZ_DEMO_MAT, ENT_DEMO_XLS

class TestPlotter(unittest.TestCase):
    """Test plot functions."""

    def setUp(self):
        plt.ion()

    def tearDown(self):
        plt.close('all')

    def test_hazard_intensity_pass(self):
        """Generate all possible plots of the hazard intensity."""
        hazard = HazardMat(HAZ_DEMO_MAT)
        myfig, _ = hazard.plot_intensity(event=36)
        self.assertIn('Event ID 36: NNN_1185106_gen5', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(event=-1)
        self.assertIn('1-largest Event. ID 3899: NNN_1190604_gen8', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(event=-4)
        self.assertIn('4-largest Event. ID 5489: NNN_1192804_gen8', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(event=0)
        self.assertIn('TC max intensity at each point', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(centr_id=59)
        self.assertIn('Centroid ID 59: (29.0, -79.0)', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(centr_id=-1)
        self.assertIn('1-largest Centroid. ID 100: (30.0, -75.0)', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(centr_id=-4)
        self.assertIn('4-largest Centroid. ID 70: (30.0, -78.0)', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(centr_id=0)
        self.assertIn('TC max intensity at each event', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_intensity(event='NNN_1192804_gen8')
        self.assertIn('NNN_1192804_gen8', myfig._suptitle.get_text())

    def test_hazard_fraction_pass(self):
        """Generate all possible plots of the hazard fraction."""
        hazard = HazardMat(HAZ_DEMO_MAT)
        myfig, _ = hazard.plot_fraction(event=36)
        self.assertIn('Event ID 36: NNN_1185106_gen5', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_fraction(event=-1)
        self.assertIn('1-largest Event. ID 11898: GORDON_gen7', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_fraction(centr_id=59)
        self.assertIn('Centroid ID 59: (29.0, -79.0)', \
                      myfig._suptitle.get_text())

        myfig, _ = hazard.plot_fraction(centr_id=-1)
        self.assertIn('1-largest Centroid. ID 80: (30.0, -77.0)', \
                      myfig._suptitle.get_text())

    def test_exposures_value_pass(self):
        """Plot exposures values."""
        myexp = ExposuresExcel(ENT_DEMO_XLS)
        myfig, _ = myexp.plot_value()
        self.assertIn('demo_today', myfig._suptitle.get_text())

    def test_impact_funcs_pass(self):
        """Plot diferent impact functions."""
        myfuncs = ImpactFuncsExcel(ENT_DEMO_XLS)
        _, myax = myfuncs.plot()
        self.assertEqual(2, len(myax))
        self.assertIn('TC 1 Tropical cyclone default', \
                      myax[0].title.get_text())
        self.assertIn('TC 3 TC Building code', myax[1].title.get_text())

        myfuncs.get_vulner('TC', 3).plot()
        myfuncs.plot(haz_type='TC')

    def test_impact_pass(self):
        """Plot impact exceedence frequency curves."""
        myent = Entity(ENT_DEMO_XLS)
        myhaz = HazardMat(HAZ_DEMO_MAT)
        myimp = Impact()
        myimp.calc(myent.exposures, myent.impact_funcs, myhaz)
        ifc = myimp.calc_freq_curve()
        myfig, _ = ifc.plot()
        self.assertIn('demo_today.xlsx x atl_prob.mat',\
                      myfig._suptitle.get_text())

        ifc2 = ImpactFreqCurve()
        ifc2.return_per = ifc.return_per
        ifc2.impact = 1.5e11 * np.ones(ifc2.return_per.size)
        ifc2.unit = 'NA'
        ifc2.label = 'prove'
        ifc.plot_compare(ifc2)

if __name__ == '__main__':
    unittest.main()