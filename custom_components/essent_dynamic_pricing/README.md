# Essent Dynamic Pricing Integration

This Home Assistant integration provides real-time electricity pricing from Essent's dynamic pricing API.

## Features

- **Current Price**: The current electricity price per kWh
- **Next Hour Price**: The price for the next hour
- **Today Average Price**: Average price for today
- **Today Minimum Price**: Lowest price for today (with time details)
- **Today Maximum Price**: Highest price for today (with time details)

## Installation

1. Copy the `essent_dynamic_pricing` folder to your `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Essent Dynamic Pricing" and add it

## Sensors

All sensors show prices in €/kWh including VAT.

### Current Price
Shows the current electricity price with additional attributes:
- Price excluding VAT
- VAT amount
- Start and end time
- Price breakdown (market price, purchasing fee, energy tax)

### Next Hour Price
Shows what the price will be in the next hour.

### Today Average/Min/Max Price
Statistics for today's prices to help you plan energy usage during cheaper hours.

## Data Source

Data is fetched from: https://www.essent.nl/api/public/tariffmanagement/dynamic-prices/v1/

The integration updates every hour automatically.

## Use Cases

- Display current and upcoming electricity prices on your dashboard
- Create automations to run appliances during cheaper hours
- Track your energy costs throughout the day
- Plan charging of electric vehicles during low-price periods
