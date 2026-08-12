<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/marisol-yake/debt-collective-loan-repayment-calc">
    <img src="https://wordpress-cdn-prod.debtcollective.org/wp-content/uploads/2021/08/24080706/logo-black-1.png" alt="Logo" height="80">
  </a>

<h3 align="center">Debt Collective Loan Repayment Calculator</h3>

  <p align="center">
    A tool made <i>by</i> debtors, <i>for</i> debtors!
    <br /><br />
    Our very own student loan repayment calculator.
    <br /><br />
    Made to estimate how much money you should be saving on Income-Driven Repayment (IDR) plans, and how to get connected to the Debt Collective's Campaign to call on legislators for a payment pause!
    <br />
    <br />
    <a href="https://github.com/marisol-yake/debt-collective-loan-repayment-calc"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://debt-collective-loan-repayment-calculator.streamlit.app/">View Demo</a>
    &middot;
    <a href="https://github.com/marisol-yake/debt-collective-loan-repayment-calc/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/marisol-yake/debt-collective-loan-repayment-calc/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


<a href="https://debt-collective-loan-repayment-calculator.streamlit.app/">
  <img src="img\calculator-screenshot.png" alt="Calculator Screen Shot" height="400">
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* Python 3.13


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/marisol-yake/debt-collective-loan-repayment-calc.git
   ```
2. Create your virtual environment
   ```sh
   python -m venv your-venv-name
   ```
3. Activate your virtual environment
   ```sh
   your-venv-name\Scripts\activate
   ```
4. Pip install dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```
5. Run the app locally
   ```sh
   streamlit run app.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Get hosted on streamlit community cloud
- [x] Create prototype of calculator (placeholder variables)
  - [x] Flag differences +-20% relative to selected payment plan.
  - [x] Handle division by zero errors
- [x] Translate EDCAP calculator logic, 1-to-1 (JS &rarr; Python)
- [x] Create working prototype of calculator (EDCAP result parity)
- [x] Implement REPAYE plan calculations
- [ ] Implement SAVE plan calculations
  - [x] Implement SAVE calculation logic
  - [ ] Tweak UI to accommodate input
- [x] Verify calculator logic against credible sources
  - Using the most credible resources I could find.
  - I am not a legal nor tax professional.
  - [x] PAYE
  - [x] REPAYE
  - [x] RAP
  - [x] ICR
  - [x] IBR
  - [x] SAVE
- [ ] Add calculation explanations (hover-hint?)
- [ ] Add AGI explainer (hover-hint?)
- [ ] Add finalized campaign language
- [ ] Add link to Data Privacy Policy
- [ ] Implement data collection procedure

<br />

See the [open issues](https://github.com/marisol-yake/debt-collective-loan-repayment-calc/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/marisol-yake/debt-collective-loan-repayment-calc/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=marisol-yake/debt-collective-loan-repayment-calc" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the AGPL-3.0. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marisol Yake (she / her) - marisol.yake@outlook.com

Project Link: [https://github.com/marisol-yake/debt-collective-loan-repayment-calc](https://github.com/marisol-yake/debt-collective-loan-repayment-calc)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Big thank you for the folks who worked on the [EDCAP Calculator](https://www.edcapny.org/resources-for-borrowers/student-loan-pathway/repayment-plan-calculator/), our work would not have been possible without you.
* Shoutouts to everyone involved in the [Debt Collective](https://debtcollective.org/) Payment Pause Campaign, team work makes the dream work.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/marisol-yake/debt-collective-loan-repayment-calc.svg?style=for-the-badge
[contributors-url]: https://github.com/marisol-yake/debt-collective-loan-repayment-calc/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/marisol-yake/debt-collective-loan-repayment-calc.svg?style=for-the-badge
[forks-url]: https://github.com/marisol-yake/debt-collective-loan-repayment-calc/network/members
[stars-shield]: https://img.shields.io/github/stars/marisol-yake/debt-collective-loan-repayment-calc.svg?style=for-the-badge
[stars-url]: https://github.com/marisol-yake/debt-collective-loan-repayment-calc/stargazers
[issues-shield]: https://img.shields.io/github/issues/marisol-yake/debt-collective-loan-repayment-calc.svg?style=for-the-badge
[issues-url]: https://github.com/marisol-yake/debt-collective-loan-repayment-calc/issues
[license-shield]: https://img.shields.io/github/license/marisol-yake/debt-collective-loan-repayment-calc.svg?style=for-the-badge
[license-url]: https://github.com/marisol-yake/debt-collective-loan-repayment-calc/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/marisol-yake
[product-screenshot]: img\calculator-screenshot.png
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
