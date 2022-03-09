# Introduction to Mobile Robotics Course Project

<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url] 
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
  <h3 align="center"> METE 4300U - Introduction to Mobile Robotics</h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is the repository for the course  METE 4300U - Introduction to Mobile Robotics.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

- ROS KINETIC (Ubuntu 16.04)

### Installation

1. Clone the repo in catkin_ws/src

   ```sh
   git clone https://github.com/B33Boy/mr.git
   ```

2. Run catkin_make

   ```sh
   cd ~/catkin_ws/
   catkin_make
   ```
 
## Usage

To run phase 1:

   ```sh
   roslaunch mr mr_phase1.launch 
   ```



### Generating requirements.txt 

run the command `./gen_pipreq.sh` from the root of the project to update the requirements.txt

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Abhi Patel - abhi.patel@ontariotechu.net
Hunter Peeters - hunter.peeters@ontariotechu.net
Matthew Bugeys - matthew.bugeya@ontariotechu.net
Pujan Parikh - pujan.parikh@ontariotechu.net

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/B33Boy/mr.svg?style=for-the-badge
[contributors-url]: https://github.com/B33Boy/mr/graphs/contributors
[license-shield]: https://img.shields.io/github/license/B33Boy/mr.svg?style=for-the-badge
[license-url]: https://github.com/B33Boy/mr/blob/main/LICENSE.txt

