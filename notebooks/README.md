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

   <img src="https://files.readme.io/1c553c3-translation.png" alt="" title="translation.png" class="border" align="" caption="" height="auto" width="auto" loading="lazy">

   <img src="https://files.readme.io/b4f6c49-translationresults.png" alt="" title="translationresults.png" class="border" align="" caption="" height="auto" width="auto" loading="lazy">

<br />

## Rabbit Holes to avoid

The following APIs say they're free, but they have been drepecated on rapid API and moved to a dedicated API server. Their APIs are technically free, however you must fill a request form stating your business case and website metrics to prove you are worthy of being a partner 😒. I've submitted requests already, but not holding my breath.

- Skyscanner API
- Google flights
- Kayak

## Recommended APIs to get you started

The following list is recommendation for quickly getting up and testing. However, please feel free to explore any API platforms and hosts that you wish.

<br />


  <img data-v-55c5b733="" src="https://rapidapi.com/cdn/images?url=https://rapidapi-prod-apis.s3.amazonaws.com/15/566ac36d294d1eb77dd8b79a7042ad/eb4a1fca3495b7a7a8ff618543b6a03b.png" width="50">

### **1.**  **Flight Data API**:

<br />

**Pros:**

- Completely free, however extra step required to get your api token (see steps below)
- Very simple endpoints
- */Cheapest tickets* end point, takes origin param, and returns cheapest tickets to multiple cities in a single get request. This should be useful for best middle ground recommendation
-  */Tickets for each day of month*, Takes origin, destination, depart_date, length(of stay)) params and returns flights for every day of month. This could be used to display dashboard/graph of prices for the month.
-  Many more endpoints to play with.

**Cons**

- Booking URL not returned
- Results can sometimes be sparse.

### **How to get api x-access token:**

1. [Sign up](https://www.travelpayouts.com/en/) for free to create an account
2. Once you have an account, go to the [dashboard](https://app.travelpayouts.com/dashboard)
3. In the side bar **click** on [Programs](https://app.travelpayouts.com/programs).
4. **Select** [Travel Payouts](https://app.travelpayouts.com/programs/0/about)
5. **Select** Accept terms radio checkmark
6. **Click** on **Join** button.
7. Once you have joined, you need create a [project](https://app.travelpayouts.com/profile/sources).
8. In the main area, **hover** your mouse over Travelpayout, then **click** on the **tools** icon to access the link generator. Heads up, the tools page takes a long time to load. Don't refresh the page.

⚠️ any issues let me know



<br />

<img data-v-2f338418="" src="https://rapidapi.com/cdn/images?url=https://rapidapi-prod-apis.s3.amazonaws.com/03d4b62f-887b-4fdf-a885-3be1baec452d.jpg" width="50">

### **2.** **Travel Advisor API**:

**Pros:**

- Freemium. Just need to subscribe first. 500 requests per month, or can upgrade to 10K requests per month for $20/mo
- Used to be the main API for tripadvisor
- returns lots of information about the flights including booking URL

**Cons**

- Currently in the process of deprecating (but still works)
- Unable to do a multiple city search from a from a single request.
One idead could be to loop through a list of of cities that we can create using the Flight data API (*/cheapest tickets*)


## Rapid API How to Guide

<br />

You can view a quick start guide video [here](https://docs.rapidapi.com/docs/consumer-quick-start-guide)

### API listing overview

<br />

<img src="https://files.readme.io/dd503b3-translate.png" alt="" title="translate.png" class="border" align="" caption="" height="auto" width="auto" loading="lazy">

Once you select your API, you are brought to the Endpoints tab of the API listing page. The Endpoints tab includes most of the information needed to get started with the API. It includes navigation, a list of endpoints, documentation of the currently selected endpoint, and code snippets to help you get started with your coding. The code snippets are available in many different programming languages, **including python**.

<br />

### Testing an API from the browser

<br />

<img src="https://files.readme.io/4574fc3-testendpoint.png" alt="" title="testendpoint.png" class="border" align="" caption="" height="auto" width="auto" loading="lazy">

Now that you have subscribed to an API plan, you will want to head back to the Endpoints tab. From here you can test the API endpoint directly in the browser by changing the input for the endpoint. When you make a request to the API by using the **Test Endpoint button**, you will see the response directly in the browser in the **results tab**
<br />

### Integrating the API into an application

<br />

<img src="https://files.readme.io/12498cc-codesnippets.png" alt="" title="codesnippets.png" class="border" align="" caption="" height="auto" width="auto" loading="lazy">

Once you find an API that you want to integrate into your application, switch to the Code Snippets tab. Select the **Python**, then **requests** and **copy** the code snippet right into your application code.
