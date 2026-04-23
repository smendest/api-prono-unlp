#!/bin/bash

curl -s http://localhost:5000/api/v1/forecasts/latest | python3 -m json.tool
