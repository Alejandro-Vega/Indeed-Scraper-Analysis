# Indeed-Scraper-Analysis

## Overview
This program uses the BeautifulSoup library to search through the job search website www.Indeed.com and scrape data regarding job listings on the site. This program will send the scraped data to a MySQL database where it will organize the data accordingly. The program can then visualize the data from the database in various forms of graphs.

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a>
    <img src="/img/most-mentioned-degrees.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Indeed Scraper Analysis</h3>

  <p align="center">
    An awesome indeed scraper that will store and analyze the results!
    <br />
    <a href="https://github.com/Alejandro-Vega/Indeed-Scraper-Analysis/issues">Report Bug</a>
    ·
    <a href="https://github.com/Alejandro-Vega/Indeed-Scraper-Analysis/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

  
<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](/img/example-scrape-1.png)

The project was used for researching the current job listings in my area for the Computer Science field. It aided me in writing a research paper that further analyzed the results gathered from the program.

Here's why I felt it needed to be created:
* It was an interesting project
* Infinitely faster than manually gathering data from the site
* I can more efficiently organize the data and convert into visuals
* Easy to use and friendly towards users who know nothing about the subject


A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

I used Python and the BeautifulSoup library to scrape all of the data. Meanwhile, SQL was used to store the data in one location. 

* [Python]
* [SQL]
* [BeautifulSoup]((https://www.crummy.com/software/BeautifulSoup/bs4/doc/))


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


### Installation

1. Clone the repo
   ```sh
   gh repo clone Alejandro-Vega/Indeed-Scraper-Analysis
   ```
2. Set up a MySQL database to store the data, although the program will still run if a database is not provided, but it will not store it anywhere 





<!-- USAGE EXAMPLES -->
## Usage

Run the program and choose from the various options in the Python console.

Options:
* Scrape the Indeed website for data
* Gather Statistics (Convert database data into graphs)

This programs takes into consideration many different topics such as degrees, interpersonal keywords, intrapersonal keywords, date, remote jobs, salary, and many more.

[![Indeed Scraper Analysis][input-example-screenshot]](/img/example-graph-1.png)


<p>
  <img src="/img/mysql-tables.png" width="60%" alt="Database tables">
</p>
<p>
  <img src="/img/mysql-posts-example-1.png" width="60%" alt="Example database result">
</p>
<p>
  <img src="/img/most-common-languages.png" width="60%" alt="Example graph 1">
</p>
<p>
  <img src="/img/most-mentioned-degrees.png" width="60%" alt="Example graph 1">
</p>
<p>
  <img src="/img/most-common-words-wordcloud.png" width="60%" alt="Example graph 1">
</p>



<!-- CONTRIBUTING -->
## Contributing

Currently not allowing for contributions from other people. Although, if you find an issue with the program feel free to open an issue request.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alejandro Vega - [LinkedIn](https://www.linkedin.com/in/alejandro--vega/) - AlejandroVega@alejandrovega.dev

Project Link: [https://github.com/Alejandro-Vega/Indeed-Scraper-Analysis](https://github.com/Alejandro-Vega/Indeed-Scraper-Analysis)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: /images/example-scrape-1.png
[input-example-screenshot]: /img/example-graph-1.png