import requests
import psycopg2
import time
import schedule
from datetime import datetime

api_url = "https://prices.azure.com/api/retail/prices"

postgres_config = {
    "host": "db",
    "database": "postgres",
    "user": "postgres",
    "password": "shah123"
}

def fetch_azure_vm_rates(api_url):
    max_retries = 100
    retry_delay = 10  # in seconds
    extracted_rates = []
    
    for attempt in range(max_retries):
        try:
            while api_url:
                print(api_url)
                response = requests.get(api_url)
                response.raise_for_status()
                json_data = response.json()
                vm_rates = json_data.get("Items", [])
                print("Hli Extracted VM Rates:")
                for vm_rate in vm_rates:
                    extracted_rate = {
                        "currencyCode": vm_rate.get("currencyCode", ""),
                        "tierMinimumUnits": vm_rate.get("tierMinimumUnits", ""),
                        "retailPrice": vm_rate.get("retailPrice", ""),
                        "unitPrice": vm_rate.get("unitPrice", ""),
                        "armRegionName": vm_rate.get("armRegionName", ""),
                        "location": vm_rate.get("location", ""),
                        "effectiveStartDate": vm_rate.get("effectiveStartDate", ""),
                        "meterId": vm_rate.get("meterId", ""),
                        "meterName": vm_rate.get("meterName", ""),
                        "productId": vm_rate.get("productId", ""),
                        "skuId": vm_rate.get("skuId", ""),
                        "productName": vm_rate.get("productName", ""),
                        "skuName": vm_rate.get("skuName", ""),
                        "serviceName": vm_rate.get("serviceName", ""),
                        "serviceId": vm_rate.get("serviceId", ""),
                        "serviceFamily": vm_rate.get("serviceFamily", ""),
                        "unitOfMeasure": vm_rate.get("unitOfMeasure", ""),
                        "type": vm_rate.get("type", ""),
                        "isPrimaryMeterRegion": vm_rate.get("isPrimaryMeterRegion", ""),
                        "armSkuName": vm_rate.get("armSkuName", "")
                    }
                    extracted_rates.append(extracted_rate)
                
                api_url = json_data.get("NextPageLink")
                
            return extracted_rates
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Azure VM rates (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    
    print("Failed to fetch Azure VM rates after multiple attempts.")
    return None

def store_vm_rates_in_db(vm_rates):
    try:
        connection = psycopg2.connect(**postgres_config)
        cursor = connection.cursor()
        for vm_rate in vm_rates:
            cursor.execute("""
                INSERT INTO azure_vm_rates (
                    currency_code, tier_minimum_units, retail_price, unit_price, arm_region_name,
                    location, effective_start_date, meter_id, meter_name, product_id,
                    sku_id, product_name, sku_name, service_name, service_id,
                    service_family, unit_of_measure, type, is_primary_meter_region, arm_sku_name,
                    run_timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                vm_rate["currencyCode"], vm_rate["tierMinimumUnits"], vm_rate["retailPrice"],
                vm_rate["unitPrice"], vm_rate["armRegionName"], vm_rate["location"],
                vm_rate["effectiveStartDate"], vm_rate["meterId"], vm_rate["meterName"],
                vm_rate["productId"], vm_rate["skuId"], vm_rate["productName"],
                vm_rate["skuName"], vm_rate["serviceName"], vm_rate["serviceId"],
                vm_rate["serviceFamily"], vm_rate["unitOfMeasure"], vm_rate["type"],
                vm_rate["isPrimaryMeterRegion"], vm_rate["armSkuName"], datetime.now()
            ))
        
        connection.commit()
        print("Stored")
    except (psycopg2.Error, Exception) as e:
        print("Error storing Azure VM rates in the database:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def fetch_and_store_rates():
    rates = fetch_azure_vm_rates(api_url)
    if rates:
        store_vm_rates_in_db(rates)
    else:
        print("Failed to fetch Azure VM rates.")


schedule.every().day.at("15:24").do(fetch_and_store_rates)

while True:
    schedule.run_pending()
    time.sleep(1)  # Sleep for a second to avoid high CPU usage
