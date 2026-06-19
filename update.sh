#!/bin/sh

fd '(Core|Tour).*pdf' -x python3 unnumber.py
