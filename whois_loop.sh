#!/bin/bash

DOMAINS=('domain1.com' 'domain2.com')

for domain in "${DOMAINS[@]}"
do
  whois $domain | grep "Registrar:"
done

