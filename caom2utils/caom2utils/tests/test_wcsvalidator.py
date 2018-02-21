# -*- coding: utf-8 -*-
# ***********************************************************************
# ******************  CANADIAN ASTRONOMY DATA CENTRE  *******************
# *************  CENTRE CANADIEN DE DONNÉES ASTRONOMIQUES  **************
#
#  (c) 2018.                            (c) 2016.
#  Government of Canada                 Gouvernement du Canada
#  National Research Council            Conseil national de recherches
#  Ottawa, Canada, K1A 0R6              Ottawa, Canada, K1A 0R6
#  All rights reserved                  Tous droits réservés
#
#  NRC disclaims any warranties,        Le CNRC dénie toute garantie
#  expressed, implied, or               énoncée, implicite ou légale,
#  statutory, of any kind with          de quelque nature que ce
#  respect to the software,             soit, concernant le logiciel,
#  including without limitation         y compris sans restriction
#  any warranty of merchantability      toute garantie de valeur
#  or fitness for a particular          marchande ou de pertinence
#  purpose. NRC shall not be            pour un usage particulier.
#  liable in any event for any          Le CNRC ne pourra en aucun cas
#  damages, whether direct or           être tenu responsable de tout
#  indirect, special or general,        dommage, direct ou indirect,
#  consequential or incidental,         particulier ou général,
#  arising from the use of the          accessoire ou fortuit, résultant
#  software.  Neither the name          de l'utilisation du logiciel. Ni
#  of the National Research             le nom du Conseil National de
#  Council of Canada nor the            Recherches du Canada ni les noms
#  names of its contributors may        de ses  participants ne peuvent
#  be used to endorse or promote        être utilisés pour approuver ou
#  products derived from this           promouvoir les produits dérivés
#  software without specific prior      de ce logiciel sans autorisation
#  written permission.                  préalable et particulière
#                                       par écrit.
#
#  This file is part of the             Ce fichier fait partie du projet
#  OpenCADC project.                    OpenCADC.
#
#  OpenCADC is free software:           OpenCADC est un logiciel libre ;
#  you can redistribute it and/or       vous pouvez le redistribuer ou le
#  modify it under the terms of         modifier suivant les termes de
#  the GNU Affero General Public        la “GNU Affero General Public
#  License as published by the          License” telle que publiée
#  Free Software Foundation,            par la Free Software Foundation
#  either version 3 of the              : soit la version 3 de cette
#  License, or (at your option)         licence, soit (à votre gré)
#  any later version.                   toute version ultérieure.
#
#  OpenCADC is distributed in the       OpenCADC est distribué
#  hope that it will be useful,         dans l’espoir qu’il vous
#  but WITHOUT ANY WARRANTY;            sera utile, mais SANS AUCUNE
#  without even the implied             GARANTIE : sans même la garantie
#  warranty of MERCHANTABILITY          implicite de COMMERCIALISABILITÉ
#  or FITNESS FOR A PARTICULAR          ni d’ADÉQUATION À UN OBJECTIF
#  PURPOSE.  See the GNU Affero         PARTICULIER. Consultez la Licence
#  General Public License for           Générale Publique GNU AfferoF
#  more details.                        pour plus de détails.
#
#  You should have received             Vous devriez avoir reçu une
#  a copy of the GNU Affero             copie de la Licence Générale
#  General Public License along         Publique GNU Affero avec
#  with OpenCADC.  If not, see          OpenCADC ; si ce n’est
#  <http://www.gnu.org/licenses/>.      pas le cas, consultez :
#                                       <http://www.gnu.org/licenses/>.
#
#  $Revision: 4 $
#
# ***********************************************************************
#
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# from astropy.wcs import Wcsprm
from caom2utils import WcsValidator, InvalidWCSError
from caom2 import artifact, wcs, chunk, part
from caom2.caom_util import TypedSet, TypedList, TypedOrderedDict


# TemporalWCS validator tests
def test_temporalwcs_validator():
    # TODO: how to adequately report errors
    timetest = TimeTestUtil()
    good_temporal_wcs = timetest.good_wcs()
    assert good_temporal_wcs.axis.function is not None

    try:
        WcsValidator.validate_temporal_wcs(good_temporal_wcs)
        WcsValidator.validate_temporal_wcs(None)
    except Exception as e:
        print(repr(e))
        assert False


def test_bad_temporalwcs():
    timetest = TimeTestUtil()
    bad_temporal_wcs = timetest.bad_wcs()

    try:
        WcsValidator.validate_temporal_wcs(bad_temporal_wcs)
    except InvalidWCSError as iwe:
        print("Expected temporal wcs failure: " + repr(iwe))
        assert True
    except Exception as e:
        print(repr(e))
        assert False


# SpatialWCS validation tests
def test_spatialwcs_validator():
    try:
        spatialtest = SpatialTestUtil()
        good_spatial_wcs = spatialtest.good_wcs()
        assert good_spatial_wcs.axis.function is not None

        WcsValidator.validate_spatial_wcs(good_spatial_wcs)

        # None is valid
        WcsValidator.validate_spatial_wcs(None)
    except Exception as e:
        print(repr(e))
        assert False


def test_invalid_spatial_wcs():
    try:
        position = None
        spatialtest = SpatialTestUtil()
        position = spatialtest.bad_wcs()
        WcsValidator.validate_spatial_wcs(position)
    except InvalidWCSError as iwe:
        print("Expected Spatial WCS error: " + repr(iwe))
        assert True
    except Exception as e:
        print(repr(e))
        assert False


# SpectralWCS validation tests
def test_spectralwcs_validator():
    try:
        energyTest = EnergyTestUtil()
        good_spectral_wcs = energyTest.good_wcs()
        assert good_spectral_wcs.axis.function is not None

        WcsValidator.validate_spectral_wcs(good_spectral_wcs)

        # Null validator is acceptable
        WcsValidator.validate_spectral_wcs(None)

    except Exception as e:
        print(repr(e))
        assert False


def test_invalid_spectral_wcs():
    try:
        energytest = EnergyTestUtil()
        energy_wcs = energytest.bad_wcs()
        WcsValidator.validate_spectral_wcs(energy_wcs)
    except InvalidWCSError as iwe:
        print("Expected Spectral WCS error: " + repr(iwe))
        assert True
    except Exception as e:
        print(repr(e))
        assert False


# Artifact tests
def test_valid_wcs():
    a = None
    try:
        a = get_test_artifact(chunk.ProductType.SCIENCE)
        WcsValidator.validate_artifact(a)
    except Exception as unexpected:
        print(repr(unexpected))
        assert False


def test_null_wcs():
    a = None
    try:
        a = get_test_artifact(chunk.ProductType.SCIENCE)
        WcsValidator.validate_artifact(a)
        c = a.parts['test_part'].chunks[0]

        # Not probably reasonable Chunks, but should still be valid
        # Different combinations of this will be represented in different data sets
        c.position = None
        WcsValidator.validate_artifact(a)

        c.position = SpatialTestUtil.good_wcs(SpatialTestUtil())
        c.energy = None
        WcsValidator.validate_artifact(a)

        c.energy = EnergyTestUtil.good_wcs(EnergyTestUtil())
        c.time = None
        WcsValidator.validate_artifact(a)

        c.time = TimeTestUtil.good_wcs(TimeTestUtil())
        c.polarization = None
        WcsValidator.validate_artifact(a)

        c.energy = None
        WcsValidator.validate_artifact(a)

        c.time = None
        WcsValidator.validate_artifact(a)

        # Assert: all WCS should be null at this step
        c.position = None
        WcsValidator.validate_artifact(a)

    except InvalidWCSError as unexpected:
        print(repr(unexpected))
        assert False


# Supporting Classes for generating test data
class TimeTestUtil:

    def __init__(self):
        pass

    def good_wcs(self):
        px = float(0.5)
        sx = float(54321.0)
        nx = 200
        ds = float(0.01)
        goodwcs = self.get_test_function(True, px, sx*nx*ds, nx, ds)
        return goodwcs

    def bad_wcs(self):
        px = float(0.5)
        sx = float(54321.0)
        nx = 200
        ds = float(0.01)

        badwcs = self.get_test_function(True, px, sx*nx*ds, nx, ds)
        badwcs.axis.function.ctype = "bla";
        return badwcs

    def get_test_function(self, complete, px, sx, nx, ds):
        axis_1d = wcs.CoordAxis1D(wcs.Axis("UTC", "d"))

        if complete:
            wcs.exposure = 300.0
            wcs.resolution = 0.1

        temporal_wcs = chunk.TemporalWCS(axis_1d)
        ref_coord = wcs.RefCoord(px, sx)
        temporal_wcs.axis.function = wcs.CoordFunction1D(nx, ds, ref_coord)
        return temporal_wcs


class SpatialTestUtil:

    def __init__(self):
        pass

    def good_wcs(self):
        px = float(0.5)
        py = float(0.5)
        sx = float(20.0)
        sy = float(10.0)
        # not used in java code although declared?
        # double dp = 1000.0;
        # double ds = 1.0;
        return self.get_test_function(px, py, sx, sy, False)

    # This is in the java code, but without the toPolygon function in python
    # is possibly irrelevant here. With the basic validator this will produce
    # a good WCS value.
    def bad_wcs(self):
        axis1 = wcs.Axis("RA---TAN", "deg")
        axis2 = wcs.Axis("DEC--TAN", "deg")
        axis = wcs.CoordAxis2D(axis1, axis2)
        spatial_wcs = chunk.SpatialWCS(axis)
        spatial_wcs.equinox = None
        dim = wcs.Dimension2D(1024, 1024)
        ref = wcs.Coord2D( wcs.RefCoord(512.0, 10.0),  wcs.RefCoord(512.0, 20.0))
        #  Create Invalid function
        axis.function = wcs.CoordFunction2D(dim, ref, 1.0e-3, 0.0, 0.0, 0.0) # singular CD matrix
        return spatial_wcs

    def get_test_function(self, px, py, sx, sy, gal):
        axis1 = wcs.Axis("RA", "deg")
        axis2 = wcs.Axis("DEC", "deg")

        if gal:
            axis1 = wcs.Axis("GLON", "deg")
            axis2 = wcs.Axis("GLAT", "deg")

        axis_2d = wcs.CoordAxis2D(axis1, axis2)

        spatial_wcs = chunk.SpatialWCS(axis_2d)
        spatial_wcs.coordsys = "ICRS"

        wcs.coordsys = "ICRS"
        if gal:
            spatial_wcs.coordsys = None

        wcs.equinox = None

        # Simple frame set: 1000x1000 pixels, 1 pixel = 1.0e-3 deg
        dim = wcs.Dimension2D(1000, 1000)
        ref = wcs.Coord2D(wcs.RefCoord(px, sx), wcs.RefCoord(py, sy))
        axis_2d.function = wcs.CoordFunction2D(dim, ref, 1.e-3, 0.0, 0.0, 1.0e-3)
        return spatial_wcs


#  TODO: add functions to create test data here
class PolarizationTestUtil:
    def __init__(self):
        pass

    def good_wcs(self):
        pass

    def bad_wcs(self):
        pass


#  TODO: Under construction
class EnergyTestUtil:
    def __init__(self):
        self.BANDPASS_NAME = "H-Alpha-narrow"
        self.TRANSITION = wcs.EnergyTransition("H", "alpha")

    def good_wcs(self):
        px = float(0.5)
        sx = float(400.0)
        nx = float(200.0)
        ds = float(1.0)
        # SpectralWCS
        energy_test_util = EnergyTestUtil();
        energy = energy_test_util.getTestRange(True, px, sx * nx * ds, nx, ds)

        c1 = wcs.RefCoord(0.5, 2000.0)
        energy.axis.function = wcs.CoordFunction1D(100, 10.0, c1)
        return energy

    def bad_wcs(self):
        px = float(0.5)
        sx = float(400.0)
        nx = 200
        ds = float(1.0)
        bad_energy = self.getTestFunction(True, px, sx * nx * ds, nx, ds)
        # Make function invalid
        c1 = wcs.RefCoord(0.5, 2000.0)
        bad_energy.axis.function = wcs.CoordFunction1D(100, 10.0, c1)
        return wcs

    def getTestRange(self, complete, px, sx, nx, ds):
        axis =  wcs.CoordAxis1D(wcs.Axis("WAVE", "nm"))
        # log.debug("test axis: " + axis);
        spectral_wcs = chunk.SpectralWCS(axis, "TOPOCENT")
        if complete:
            spectral_wcs.bandpassName = self.BANDPASS_NAME
            spectral_wcs.restwav = 6563.0e-10 # meters
            spectral_wcs.resolvingPower = 33000.0
            spectral_wcs.transition = self.TRANSITION

        c1 = wcs.RefCoord(px, sx)
        c2 = wcs.RefCoord(px + nx, sx + nx * ds)
        spectral_wcs.axis.range = wcs.CoordRange1D(c1, c2)
        # log.debug("test range: " + axis.range)
        return spectral_wcs

    def getTestFunction(self, complete, px, sx, nx, ds):
        axis = wcs.CoordAxis1D(wcs.Axis("WAVE", "nm"))
        # log.debug("test axis: " + axis);
        spectral_wcs = chunk.SpectralWCS(axis, "TOPOCENT")
        if complete:
            spectral_wcs.bandpassName = self.BANDPASS_NAME
            spectral_wcs.restwav = 6563.0e-10; # meters
            spectral_wcs.resolvingPower = 33000.0
            spectral_wcs.transition = self.TRANSITION

        c1 = wcs.RefCoord(px, sx)
        spectral_wcs.axis.function = wcs.CoordFunction1D(nx, ds, c1)
        # log.debug("test function: " + axis.function)
        return spectral_wcs


def get_good_test_chunk(ptype):
    test_chunk = chunk.Chunk()
    test_chunk.position = SpatialTestUtil.good_wcs(SpatialTestUtil())
    test_chunk.energy = EnergyTestUtil.good_wcs(EnergyTestUtil())
    test_chunk.time = TimeTestUtil.good_wcs(TimeTestUtil())
    test_chunk.polarization = PolarizationTestUtil.good_wcs(PolarizationTestUtil())

    return test_chunk


# Under construction
def get_test_artifact(ptype):
    # chunk.ProductType.SCIENCE is a common type
    if ptype is None:
        ptype = chunk.ProductType.SCIENCE
    test_artifact = artifact.Artifact('uri:foo/bar', ptype, artifact.ReleaseType.DATA)
    chunks = TypedList(chunk.Chunk)
    chunks.append(get_good_test_chunk(ptype))

    test_part = part.Part("test_part", ptype, chunks)
    test_artifact.parts = TypedOrderedDict(part.Part)
    test_artifact.parts['test_part'] = test_part

    return test_artifact
