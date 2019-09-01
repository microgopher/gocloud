#!/bin/sh

redis-cli -h $REDIS_HOST -p 6379 set api:/api/auth $USERS_SERVICE_HOST/auth
redis-cli -h $REDIS_HOST -p 6379 set api:/api/providers $PROVIDERS_SERVICE_HOST/providers
redis-cli -h $REDIS_HOST -p 6379 set api:/api/customers $CUSTOMERS_SERVICE_HOST/customers
redis-cli -h $REDIS_HOST -p 6379 set api:/api/users $USERS_SERVICE_HOST/users