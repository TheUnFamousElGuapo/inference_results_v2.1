# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
sys.path.insert(0, os.getcwd())

from code.common.constants import Benchmark, Scenario
from code.common.systems.system_list import KnownSystem
from configs.configuration import *
from configs.resnet50 import GPUBaseConfig, CPUBaseConfig


class OfflineGPUBaseConfig(GPUBaseConfig):
    scenario = Scenario.Offline

    run_infer_on_copy_streams = False
    use_graphs = False
    gpu_inference_streams = 1
    gpu_copy_streams = 2


class OfflineCPUBaseConfig(CPUBaseConfig):
    scenario = Scenario.Offline


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class NC96ads_A100_v4(OfflineGPUBaseConfig):
    system = KnownSystem.NC96ads_A100_v4
    gpu_batch_size = 2048
    offline_expected_qps = 37000 * 4


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class NC96ads_A100_v4_Triton(NC96ads_A100_v4):
    use_triton = True


@ConfigRegistry.register(HarnessType.LWIS, AccuracyTarget.k_99, PowerSetting.MaxP)
class ND96amsr_A100_v4(OfflineGPUBaseConfig):
    system = KnownSystem.ND96amsr_A100_v4
    gpu_batch_size = 2048
    start_from_device = True
    run_infer_on_copy_streams = True
    gpu_inference_streams = 2
    gpu_copy_streams = 3
    offline_expected_qps = 340000


@ConfigRegistry.register(HarnessType.Triton, AccuracyTarget.k_99, PowerSetting.MaxP)
class ND96amsr_A100_v4_Triton(ND96amsr_A100_v4):
    start_from_device = None
    gpu_copy_streams = 1
    num_concurrent_batchers = 6
    num_concurrent_issuers = 6
    instance_group_count = 2
    batch_triton_requests = True
    use_triton = True
    offline_expected_qps = 310000

