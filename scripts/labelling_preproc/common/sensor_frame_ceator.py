#!/usr/bin/python3

from labelling_preproc.common.sample_formats import (
    image_struct,
    pcd_struct,
    fsp_l_struct,
    rsp_l_struct,
    lspf_r_struct,
    lspr_l_struct,
    rspf_l_struct,
    rspr_r_struct,
)


class SensorFrameCreator:

    def __init__(self):
        # Based on vehicle's TF tree
        self.GROUND_Z_OFFSET_BELOW_LIDAR_M = -1.78

    def create_3dpointcloud_frame(
        self, idx, sync_key_frame, assets_meta, ego_poses
    ):
        # Initialise frame with the template struct
        pointcloud_frame = pcd_struct

        # Set LIDAR url
        lidar_asset_id = str(sync_key_frame['lidar']['global_id'])
        pointcloud_frame['pcd']['url'] = assets_meta[lidar_asset_id]['s3_url']

        # Set frame timestamp
        total_nanosec = (
            sync_key_frame['stamp']['sec'] * (10**9)
            + sync_key_frame['stamp']['nanosec']
        )
        pointcloud_frame['timestamp'] = str(total_nanosec)

        # Set frame name based on index
        pointcloud_frame['name'] = 'frame_' + str(idx)

        # Get and set ego pose based on index
        pointcloud_frame['ego_pose'] = ego_poses.getEgoPose(idx)

        # Get and Set images based on metadata
        pointcloud_frame['images'] = self.get_images(
            sync_key_frame, assets_meta
        )

        # Set ground height offset relative to the lidar
        pointcloud_frame['default_z'] = self.GROUND_Z_OFFSET_BELOW_LIDAR_M

        return pointcloud_frame

    def create_image_frame(self, idx, cam_meta, assets_meta):
        image_frame = image_struct
        # Get url based on camera's image global id
        img_asset_id = str(cam_meta['global_id'])
        url = assets_meta[img_asset_id]['s3_url']
        image_frame['image']['url'] = url
        image_frame['name'] = 'frame_' + str(idx)

        return image_frame

    def get_cam_url(self, camera_name, cameras_list, assets_meta):

        cam_id = None
        for camera in cameras_list:
            if camera['name'] == camera_name:
                cam_id = camera['global_id']

        if cam_id is None:
            return 'S3 url not found!'

        return assets_meta[str(cam_id)]['s3_url']

    def get_images(self, sync_key_frame, assets_meta):

        # FIXME: Simplify this (see #3)
        sample = dict()
        sample["images"] = [
            fsp_l_struct,
            rsp_l_struct,
            lspf_r_struct,
            lspr_l_struct,
            rspf_l_struct,
            rspr_r_struct,
        ]

        sample["images"][0]["url"] = self.get_cam_url(
            'fsp_l', sync_key_frame['cameras'], assets_meta
        )
        sample["images"][1]["url"] = self.get_cam_url(
            'rsp_l', sync_key_frame['cameras'], assets_meta
        )
        sample["images"][2]["url"] = self.get_cam_url(
            'lspf_r', sync_key_frame['cameras'], assets_meta
        )
        sample["images"][3]["url"] = self.get_cam_url(
            'lspr_l', sync_key_frame['cameras'], assets_meta
        )
        sample["images"][4]["url"] = self.get_cam_url(
            'rspf_l', sync_key_frame['cameras'], assets_meta
        )
        sample["images"][5]["url"] = self.get_cam_url(
            'rspr_r', sync_key_frame['cameras'], assets_meta
        )

        return sample["images"]
