<img class="header-image is-logo-image" alt="RapidAPI" src="https://rapidapi.com/wp-content/uploads/2021/07/Brand-blue-horizontal.svg" title="RapidAPI">

# Getting Started with Rapid API

## About rapid API

Search and Find the Right API for Your Application

Sign up for a free account and discover the APIs that work best for your project or application. With RapidAPI you can:

Establish one location for all your APIs and avoid having to search multiple sites
Choose APIs by reviewing the popularity score, average latency, and average success rate directly in the search results

Browse APIs by category, collection, or type by using the dropdown menu, search bar, or RapidAPI’s collections (a grouping of APIs based on similar or complementary functionality)

<br />

## Quick start guide

1. [Sign up to create a account](https://rapidapi.com/auth/sign-up?referral=/hub)
2. Navigate to the [RapidAPI Hub](https://rapidapi.com/hub) where you can discover and connect to thousands of APIs
3. When you find an API that like, click the bookmark icon  <img data-v-689d684c="" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDE0IDE2Ij4KICAgIDxwYXRoIGZpbGw9IiNBRENDRjEiIGZpbGwtcnVsZT0iZXZlbm9kZCIgc3Ryb2tlPSIjNEE5MEUyIiBkPSJNMSAxLjk0NVYxNS41bDUuOTgyLTUuNDgyTDEzIDE1LjVWMS45NDVDMTMgMS4xNDcgMTIuMzUzLjUgMTEuNTU1LjVoLTkuMTFDMS42NDcuNSAxIDEuMTQ3IDEgMS45NDV6Ii8+Cjwvc3ZnPgo=" id="save_product_btn_57f1ff38e4b0036abc9166f2"> next to the title at the top.

   You can access your saved apis by selecting your profile icon, then **Saved APIs**.

<br />

## Rabbit Holes to avoid:

The following APIs say free, but they no longer exist on rapid API and have been moved to their own dedicated API server. Their APIs are technically free, however you need to fill a request form providing your business case and website metrics to prove you are worthy of being a partner 😒. I've submitted a requests already, but not holding my breath.

- Skyscanner API
- Google flights
- Kayak

## Recommended APIs to get you started:

The following list is recommendation for quickly getting up and testing. However please feel free to explore any API platforms and hosts that you wish.

<br />

  <img data-v-55c5b733="" src="https://rapidapi.com/cdn/images?url=https://rapidapi-prod-apis.s3.amazonaws.com/15/566ac36d294d1eb77dd8b79a7042ad/eb4a1fca3495b7a7a8ff618543b6a03b.png" width="50">

### **Flight Data API**:

<br />

**Pros:**

- Completely free, however extra step required to get your api token.
- Very simple endpoints
- */Cheapest tickets* end point, takes origin param, and returns cheapest tickets to multiple cities in a single get request. This should be useful for best middle ground recommendation
-  */Tickets for each day of month*, Takes origin, destination, depart_date, length(of stay)) params and returns flights for every day of month. This could be used to display dashboard/graph of prices for the month.
-  Many more endpoints to play with.

**Cons**

- Booking URL not returned
- Results can sometimes be sparse.
-
<br />

**How to guide**



<img data-v-2f338418="" src="https://rapidapi.com/cdn/images?url=https://rapidapi-prod-apis.s3.amazonaws.com/03d4b62f-887b-4fdf-a885-3be1baec452d.jpg" width="50">

### **Travel Advisor API**:

**Pros:**

- Freemium. Just need to subscribe first. 500 requests per month, or can upgrade to 10K requests per month for $20/mo
- Used to be the main API for tripadvisor
- returns lots information about the flights including booking URL

**Cons**

- Currently in the process of deprecating.
- Unable to to do a multiple city search from a single origin from a single request.
May have loop through a list of of cities that we can create using the Flight data API (*/cheapest tickets*)
