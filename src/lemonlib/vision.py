from __future__ import annotations

from photonlibpy.photonCamera import PhotonCamera, setVersionCheckEnabled
from photonlibpy.targeting.photonPipelineResult import PhotonPipelineResult
from robotpy_apriltag import AprilTagFieldLayout

from wpimath.geometry import Transform3d, Pose2d, Pose3d


class LemonCamera(PhotonCamera):
    """
    Wrapper for photonlibpy PhotonCamera.
    """
    def __init__(
        self,
        name: str,
        camera_to_bot: Transform3d,
        april_tag_field: AprilTagFieldLayout,
        version_check: bool = True,
    ) -> None:
        """
        Initializes `LemonCamera`.

        Args:
            name: The name of the camera in PhotonVision.
            camera_to_bot: A `Transform3d` that maps camera space to robot space
            april_tag_field: The locations of april tags for the camera.
            version_check: Whether to check the camera version during initialization or not.
        """
        PhotonCamera.__init__(self, name)
        self.camera_to_bot = camera_to_bot
        self.april_tag_field = april_tag_field
        setVersionCheckEnabled(version_check)

        self._results: list[PhotonPipelineResult] = []
        self._last_valid_tag: int | None = None

    def update(self) -> None:
        """
        Updates the camera state and internal results list from the camera.
        """
        self._results = self.getAllUnreadResults()

    def has_target(self) -> bool:
        """
        Returns true if wthe camera currently sees a target.
        """
        return len(self._results) > 0 and self._results[-1].hasTargets()

    def get_best_tag(self) -> int | None:
        if self._results:
            result = self._results[-1]
            best_target = result.getBestTarget()
            if best_target is not None:
                self._last_valid_tag = best_target.getFiducialId()
                return self._last_valid_tag
        return self._last_valid_tag

    def get_tag_pose(self, ID: int, twod: bool) -> Pose2d | Pose3d | None:
        if twod:
            pose = self.april_tag_field.getTagPose(ID)
            if pose is None:
                return None
            return pose.toPose2d()
        else:
            return self.april_tag_field.getTagPose(ID)

    def get_best_pose(self, twod: bool = True) -> Pose2d | Pose3d | None:
        best_tag = self.get_best_tag()
        if best_tag is None:
            return None
        tag_pose = self.april_tag_field.getTagPose(best_tag)
        if tag_pose is None:
            return None
        if twod:
            return tag_pose.toPose2d()
        return tag_pose
