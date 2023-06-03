#!/bin/bash

echo "GET https://ms-user.authme.localhost/auth/vegeta" | ./vegeta attack -duration=${1}s -insecure | ./vegeta report