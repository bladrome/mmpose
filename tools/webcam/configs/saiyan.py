# Copyright (c) OpenMMLab. All rights reserved.
runner = dict(
    # Basic configurations of the runner
    name='Human Pose and Effects',
    camera_id=0,
    camera_fps=30,

    # Define user buffers
    # Each user buffer is defined by buffer_name (str) or
    # Tuple[buffer_name (str), buffer_size(int)]
    # Note that there are also runner-reserved buffers which are not listed
    # here. You can find them in the node configs below. For example:
    #   - '_frame_': reserved buffer that stores input video frames
    #   - '_input_': reserved buffer that stores video frames for model input
    #   - '_display_': reserved buffer that stores output frames for display
    user_buffers=[
        'det_result', 'pose_result', 'frame', 'vis_pose', 'vis_moustache',
        'vis_saiyan', 'vis'
    ],

    # Define nodes.
    #
    # The configuration of a node usually includes:
    #   1. 'type': Node class name
    #   2. 'name': Node name
    #   3. I/O buffers (e.g. 'input_buffer', 'output_buffer'): specify the
    #       input and output buffer names. This may depend on the node class.
    #   4. 'enable_key': assign a hot-key to toggle enable/disable this node.
    #       This may depend on the node class.
    #   5. Other class-specific arguments
    nodes=[
        # 'DetectorNode':
        # This node performs object detection from the frame image using an
        # MMDetection model.
        dict(
            type='DetectorNode',
            name='Detector',
            model_config='demo/mmdetection_cfg/'
            'ssdlite_mobilenetv2_scratch_600e_coco.py',
            model_checkpoint='https://download.openmmlab.com'
            '/mmdetection/v2.0/ssd/'
            'ssdlite_mobilenetv2_scratch_600e_coco/ssdlite_mobilenetv2_'
            'scratch_600e_coco_20210629_110627-974d9307.pth',
            input_buffer='_input_',  # `_input_` is a runner-reserved buffer
            output_buffer='det_result'),
        # 'TopDownPoseEstimatorNode':
        # This node performs keypoint detection from the frame image using an
        # MMPose top-down model. Detection results is needed.
        dict(
            type='TopDownPoseEstimatorNode',
            name='TopDown Pose Estimator',
            model_config='configs/wholebody/2d_kpt_sview_rgb_img/'
            'topdown_heatmap/coco-wholebody/'
            'vipnas_mbv3_coco_wholebody_256x192_dark.py',
            model_checkpoint='https://openmmlab-share.oss-cn-hangz'
            'hou.aliyuncs.com/mmpose/top_down/vipnas/vipnas_mbv3_co'
            'co_wholebody_256x192_dark-e2158108_20211205.pth',
            cls_names=['person'],
            input_buffer='det_result',
            output_buffer='pose_result'),
        # 'ModelResultBindingNode':
        # This node binds the latest model inference result with the current
        # frame. (This means the frame image and inference result may be
        # asynchronous).
        dict(
            type='ModelResultBindingNode',
            name='ResultBinder',
            synchronous=False,
            frame_buffer='_frame_',  # `_frame_` is a runner-reserved buffer
            result_buffer='pose_result',
            output_buffer='frame'),
        # 'PoseVisualizerNode':
        # This node draw the pose visualization result in the frame image.
        # Pose results is needed.
        dict(
            type='PoseVisualizerNode',
            name='Visualizer',
            enable_key='v',
            frame_buffer='frame',
            output_buffer='vis_pose'),
        # 'SaiyanNode':
        # This node draw the hat effect in the frame image.
        # Pose results is needed.
        dict(
            type='SaiyanNode',
            name='Visualizer',
            enable_key='s',
            frame_buffer='vis_pose',
            output_buffer='vis_saiyan'),
        # 'MoustacheNode':
        # This node draw the moustache effect in the frame image.
        # Pose results is needed.
        dict(
            type='MoustacheNode',
            name='Visualizer',
            enable_key='c',
            frame_buffer='vis_saiyan',
            output_buffer='vis_moustache'),
        # 'BillboardNode':
        # This node show a billboard with given content, e.g. help
        # information.
        dict(
            type='BillboardNode',
            name='Help Information',
            enable_key='h',
            frame_buffer='vis_moustache',
            output_buffer='vis',
            content_lines=[
                'This is a demo for pose visualization and simple image '
                'effects. Have fun!', '', 'Hot-keys:',
                '"v": Pose estimation result visualization',
                '"s": Saiyan effect', '"c": Moustache effect',
                '"h": Show help information',
                '"m": Show diagnostic information', '"q": Exit'
            ],
        ),
        # 'MonitorNode':
        # This node show diagnostic information in the frame image. It can
        # be used for debugging or monitoring system resource status.
        dict(
            type='MonitorNode',
            name='Monitor',
            enable_key='m',
            style='fancy',
            frame_buffer='vis',
            output_buffer='_display_')  # `_frame_` is a runner-reserved buffer
    ])
