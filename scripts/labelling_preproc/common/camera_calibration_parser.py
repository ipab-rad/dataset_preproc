"""Camera calibration parser."""

import yaml
from dataclasses import dataclass


@dataclass
class Intrinsics:
    """
    Pinhole camera intrinsic values

    fx, fy: focal length in pixels
    cx, cy: offsets (in pixels) ofgit stat the principal point
            from the top-left corner of the image
    """

    fx: float
    fy: float
    cx: float
    cy: float


@dataclass
class Distortion:
    """
    Brown-Conrady distortion coefficients

    k1, k2, k3: radial distortion coefficients
    p1, p2: tangential distortion coefficients
    """

    model: str
    k1: float
    k2: float
    k3: float
    p1: float
    p2: float


@dataclass
class CameraCalibrationData:
    """
    Camera calibration data

    frame_id: camera frame id
    intrinsics: camera intrinsic values
    distortion: camera distortion coefficients
    """

    frame_id: str
    intrinsics: Intrinsics
    distortion: Distortion


class CameraCalibrationParser:
    """
    Camera calibration params parser
    """

    def __init__(self):
        pass

    def get_intrinsics(self, camera_matrix: dict) -> Intrinsics:
        """
        Parse the camera matrix and return the intrinsic values.

        Args:
            camera_matrix (dict): Dictionary containing the 'data' list with intrinsic values.

        Returns:
            Intrinsics: Parsed intrinsic parameters.
        """
        # data = [fx, 0, cx, 0, fy, cy, 0, 0, 1]
        fx = camera_matrix['data'][0]
        cx = camera_matrix['data'][2]
        fy = camera_matrix['data'][4]
        cy = camera_matrix['data'][5]
        return Intrinsics(fx, fy, cx, cy)

    def get_distortion(self, distortion_coeffs: dict) -> Distortion:
        """
        Parse the distortion coefficients and return the distortion values.

        Args:
            distortion_coeffs (dict): Dictionary containing the 'data' list with distortion values.

        Returns:
            Distortion: Parsed distortion parameters.
        """
        # data = [k1, k2, t1, t2, k3]
        k1 = distortion_coeffs['data'][0]
        k2 = distortion_coeffs['data'][1]
        p1 = distortion_coeffs['data'][2]
        p2 = distortion_coeffs['data'][3]
        k3 = distortion_coeffs['data'][4]
        return Distortion('brown-conrady', k1, k2, k3, p1, p2)

    def get_camera_calibration(
        self, camera_calibration_file: str
    ) -> CameraCalibrationData:
        """
        Parse the camera intrinsics file and return the calibration data.

        Args:
            camera_calibration_file (str): Path to the YAML file containing camera calibration parameters.

        Returns:
            CameraCalibrationData: Full calibration data including frame ID, intrinsics, and distortion.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            KeyError: If expected keys are missing in the YAML data.
            yaml.YAMLError: If the YAML content is invalid.
        """
        with open(camera_calibration_file) as yaml_file:
            camera_calibration = yaml.safe_load(yaml_file)

            intrinsics = self.get_intrinsics(
                camera_calibration['camera_matrix']
            )
            distortion = self.get_distortion(
                camera_calibration['distortion_coefficients']
            )

            frame_id = camera_calibration['camera_frame_id']
            return CameraCalibrationData(frame_id, intrinsics, distortion)
