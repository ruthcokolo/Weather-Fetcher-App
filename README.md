# Weather Fetcher App

A Python-based desktop application built with PyQt5 that fetches and displays real-time weather data using the OpenWeatherMap API.

## Features
- Real-time weather data retrieval
- User-friendly PyQt5 graphical interface
- Asynchronous, multi-threaded data fetching to keep the UI responsive
- Caching to reduce redundant API calls
- Periodic weather updates
- Performance profiling using cProfile

## Technologies Used
- Python
- PyQt5
- OpenWeatherMap API
- Multithreading
- cProfile

## Key Engineering Concepts
- REST API integration with error handling
- Multi-threaded background tasks to prevent UI blocking
- Performance optimization through caching
- Profiling and performance analysis using cProfile

## How It Works
The application fetches weather data from the OpenWeatherMap API in a background thread while updating the GUI safely on the main thread. Cached responses are reused where possible to improve performance and reduce network usage.

## Future Improvements
- Improved UI styling
- Additional weather metrics
- Enhanced error handling and logging