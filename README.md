[<img alt="PyPI" src="https://img.shields.io/pypi/v/anedya-nexus-sdk?style=for-the-badge">](https://pypi.org/project/anedya-nexus-sdk/)&nbsp;&nbsp;[<img alt="Anedya Documentation" src="https://img.shields.io/badge/Anedya-Documentation-blue?style=for-the-badge">](https://docs.anedya.io?utm_source=github&utm_medium=link&utm_campaign=github-nexus-sdk-python&utm_content=python)


 <!---<div style="width:20%; margin:0 auto;margin-bottom:50px;margin-top:50px;">-->
<p align="center">
    <img src="https://cdn.anedya.io/anedya_black_banner.png" alt="Logo">
</p>
<!--</div>-->

# Anedya Nexus SDK for Python

The Anedya Nexus SDK lets Python applications communicate with Anedya Cloud, including from within a spark function runtime.
It currently provides a synchronous client for submitting variable readings
over gRPC (the default) or HTTP.

## Install

```bash
pip install anedya-nexus-sdk
```

## Quick start

Set your API key in the environment rather than hard-coding it in your
application:

```bash
export ANEDYA_API_KEY="your-api-key"
```
> 
> ### Note:
> If initializing the SDK from a Spark function, SDK automatically inherits the authentication context from the Spark runtime, so you do not need to set an API key in that case.


Then submit a variable reading:

```python
import time

from anedya.nexus import AnedyaClient, VariableReading

reading = VariableReading(
    node_id="your-node-id",
    variable="temperature",
    timestamp=int(time.time() * 1000),
    float_value=23.5,
)

with AnedyaClient() as client:
    response = client.data_management.submit_data(reading)

if not response.success:
    raise RuntimeError(
        f"Data submission failed: {response.error_message} "
        f"({response.reason_code})"
    )
```

`timestamp` is a Unix timestamp in milliseconds. You can also pass an API key directly with `AnedyaClient(api_key="...")`.

To configure a custom domain, pass `base_url` to `AnedyaClient`. To use HTTP instead of gRPC, pass `transport="http"`.

## Links

- [Anedya documentation](https://docs.anedya.io)
- [GitHub repository](https://github.com/anedyaio/anedya-nexus-sdk-python)
- [License](./LICENSE) (Apache-2.0)
