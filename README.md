# US Crime Insight

**US Crime Insight** is an open, extensible platform that automates the collection, enrichment, and analysis of publicly available crime data across the United States. It aims to help cities, researchers, analysts, and citizens better understand local crime trends through clean, structured, and geospatially enriched datasets.

---

## 📌 Project Objective

The goal of this project is to:

- Aggregate crime data from multiple US city open data portals
- Standardize and enrich address data using geocoding techniques
- Provide clean datasets for visual analysis, policymaking, and public insight
- Lay the foundation for a scalable crime-mapping and analytics platform

---

## ✅ Advantages

- **Automated & Reproducible**: The system can be scheduled or triggered to update datasets regularly with minimal manual intervention.
- **Modular Design**: New cities and data sources can be added with minimal effort.
- **Geospatial Enrichment**: Converts public addresses to precise coordinates for better mapping and analysis.
- **Audit-Ready Logging**: Maintains logs of all preprocessing operations for transparency and QA.
- **Scalable Foundation**: Future-ready to plug into dashboards, cloud databases, or APIs.

---

## ⚠️ Limitations & Considerations

- **API Quotas**: Geocoding depends on Google Maps API, which has daily and rate limits.
- **Data Variability**: Each city's open data format and update frequency varies and may require custom handling.
- **Not Real-Time**: The platform operates on batch updates (e.g., daily, weekly), not live streams.

---

## 🚀 Future Scope

- Add real-time or scheduled cloud-based ingestion pipelines (e.g., GCP, Azure)
- Integrate interactive dashboards and geospatial visualizations
- Apply clustering and predictive analytics for crime pattern forecasting
- Expand support to hundreds of city/county datasets nationwide
- Offer public API endpoints for civic developers or researchers

---

## 🤝 Contributions

We welcome meaningful contributions to expand this platform.

You can:
- Add support for a new city dataset
- Improve data quality or performance of the geocoding logic
- Suggest or implement visualizations and analysis modules
- Report bugs or propose architectural improvements

Please fork the repo and open a pull request or raise an issue if you have ideas.

---

## 📚 Citation & Credits

This project utilizes:

- Public datasets from [City of Denton Open Data Portal](https://data.cityofdenton.com/)
- Geocoding via the [Google Maps API](https://developers.google.com/maps/documentation/geocoding/)
- Built and maintained using Python and open-source libraries like `pandas`, `geopy`, and `openpyxl`

If you use this project in your research or application, feel free to cite it or mention the GitHub repository.

---

## 🧑‍💻 Maintainer

**Sateesh Gurijala**  
This is a personal long-term project meant to showcase practical data engineering and analytics capabilities.  
It’s also a foundation for building civic-tech tools that help cities and citizens alike.

---

