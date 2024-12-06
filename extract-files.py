#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/mido',
    'hardware/qcom-caf/msm8953',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None
lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    ('libwpa_client'): lib_fixup_remove,
}

# Define the blob fixups
blob_fixups: blob_fixups_user_type = {
    'vendor/bin/gx_fpd': blob_fixup()
        .remove_needed('libunwind.so')
        .remove_needed('libbacktrace.so')
        .add_needed('libshims_gxfpd.so')
        .add_needed('fakelogprint.so'),
    'vendor/bin/mm-qcamera-daemon': blob_fixup()
        .regex_replace(r'/data/misc/camera/cam_socket', r'/data/vendor/qcam/cam_socket'),
    'vendor/lib/libchromaflash.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libmmcamera2_sensor_modules.so': blob_fixup()
        .regex_replace(r'/system/etc/camera', r'/vendor/etc/camera'),
    ('vendor/lib/libmmcamera2_cpp_module.so', 'libmmcamera2_dcrf.so', 'libmmcamera2_iface_modules.so', 'libmmcamera2_imglib_modules.so', 'libmmcamera2_mct.so', 'libmmcamera2_pproc_modules.so', 'libmmcamera2_q3a_core.so', 'libmmcamera2_sensor_modules.so', 'libmmcamera2_stats_algorithm.so', 'libmmcamera2_stats_modules.so', 'libmmcamera_dbg.so', 'libmmcamera_imglib.so', 'libmmcamera_pdafcamif.so', 'libmmcamera_pdaf.so', 'libmmcamera_tintless_algo.so', 'libmmcamera_tintless_bg_pca_algo.so', 'libmmcamera_tuning.so'): blob_fixup()
        .regex_replace(r'/data/misc/camera/', r'/data/vendor/qcam/'),
    'vendor/lib/libmmcamera_dbg.so': blob_fixup()
        .regex_replace(r'persist.camera.debug.logfile', r'persist.vendor.camera.dbglog'),
    'vendor/lib/libmmcamera_hdr_gb_lib.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libmmcamera_ppeiscore.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/lib/libmmcamera_tuning.so' : blob_fixup()
        .remove_needed('libmm-qcamera.so'),
    'vendor/lib/libmmcamera2_stats_modules.so': blob_fixup()
        .remove_needed('libandroid.so')
        .remove_needed('libgui.so')
        .regex_replace(r'libandroid.so', r'libcamshim.so'),
    'vendor/lib/libmpbase.so': blob_fixup()
        .remove_needed('libandroid.so')
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/liboptizoom.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libseemore.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libstagefright_soft_ddpdec.so': blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib/libtrueportrait.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libubifocus.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libdlbdsservice.so': blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib64/libfp_client.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfpnav.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libfpservice.so': blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib64/libril-qc-hal-qmi.so': blob_fixup()
        .regex_replace(r'android.hardware.radio.config@1.0.so', r'android.hardware.radio.c_shim@1.0.so')
        .regex_replace(r'android.hardware.radio.config@1.1.so', r'android.hardware.radio.c_shim@1.1.so')
        .regex_replace(r'android.hardware.radio.config@1.2.so', r'android.hardware.radio.c_shim@1.2.so'),
    'vendor/lib64/libthermalfeature.so': blob_fixup()
        .regex_replace(r'system/etc/', r'vendor/etc/'),
    ('vendor/lib64/hw/fingerprint.goodix.so', 'gxfingerprint.default.so'): blob_fixup()
        .add_needed('fakelogprint.so'),
    'system_ext/lib64/lib-imscamera.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/lib-imsvideocodec.so': blob_fixup()
        .add_needed('libgui_shim.so')
        .replace_needed('libqdMetaData.so', 'libqdMetaData.system.so'),
     ('vendor/lib/libmmcamera_dbg.so', 'libmmcamera_pdafcamif.so', 'libmmcamera_pdaf.so', 'libmmcamera_imx258_mono.so', 'libjpegehw.so', 'libjpegdhw.so', 'libmmcamera_hdr_gb_lib', 'libmmcamera_imx258_ofilm', 'libmmcamera_imx258_sunny', 'libmmcamera2_sensor_modules.so', 'libjpegdmahw.so', 'libmmcamera_imx258.so', 'libmmcamera_imx258_qtech.so', 'libmmcamera_le2464c_master_eeprom', 'libmmcamera_tintless_bg_pca_algo.so', 'libqomx_jpegenc.so', 'libqomx_jpegdec.so', 'libqomx_jpegenc_pipe.so') : blob_fixup()
        .add_needed('liblog.so'),
     ('vendor/lib64/libfp_client.so', 'libfpservice.so') : blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/libfpservice.so' : blob_fixup()
        .add_needed('libbinder_shim.so'),
}  # fmt: skip

# Define the module
module = ExtractUtilsModule(
    'mido',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
