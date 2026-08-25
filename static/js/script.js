/*==========================================
        VEERA VAANJI MARTIAL ARTS
        script.js
==========================================*/

// ==========================
// Sticky Navbar
// ==========================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 80) {

        navbar.classList.add("shadow");

    } else {

        navbar.classList.remove("shadow");

    }

});


// ==========================
// Back To Top Button
// ==========================

const topBtn = document.querySelector(".top-btn");

window.addEventListener("scroll", function () {

    if (window.scrollY > 400) {

        topBtn.style.display = "flex";

    } else {

        topBtn.style.display = "none";

    }

});


// ==========================
// Smooth Scrolling
// ==========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


// ==========================
// Counter Animation
// ==========================

const counters = document.querySelectorAll(".counter");

const speed = 80;

function startCounter() {

    counters.forEach(counter => {

        const target = parseInt(counter.innerText);

        let count = 0;

        const update = () => {

            const increment = target / speed;

            if (count < target) {

                count += increment;

                counter.innerText = Math.ceil(count) + "+";

                setTimeout(update, 20);

            } else {

                counter.innerText = target + "+";

            }

        };

        update();

    });

}

let counterStarted = false;

window.addEventListener("scroll", () => {

    const achievement = document.querySelector(".achievement-section");

    if (!achievement) return;

    const position = achievement.offsetTop - 400;

    if (window.scrollY > position && !counterStarted) {

        startCounter();

        counterStarted = true;

    }

});


// ==========================
// Gallery Hover Effect
// ==========================

const gallery = document.querySelectorAll(".gallery-card");

gallery.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0)";

    });

});


// ==========================
// Navbar Active Link
// ==========================

const sections = document.querySelectorAll("section");

const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 150;

        const sectionHeight = section.clientHeight;

        if (pageYOffset >= sectionTop) {

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link => {

        link.classList.remove("active");

        if (link.getAttribute("href") == "#" + current) {

            link.classList.add("active");

        }

    });

});


// ==========================
// Contact Form
// ==========================

const form = document.querySelector(".contact-form");

if (form) {

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        alert("✅ Thank you! Your message has been sent successfully.");

        form.reset();

    });

}


// ==========================
// Button Ripple Effect
// ==========================

const buttons = document.querySelectorAll(".btn,.join-btn,.course-btn");

buttons.forEach(button => {

    button.addEventListener("mouseenter", () => {

        button.style.transform = "scale(1.05)";

    });

    button.addEventListener("mouseleave", () => {

        button.style.transform = "scale(1)";

    });

});


// ==========================
// Image Fade-in
// ==========================

const images = document.querySelectorAll("img");

const imageObserver = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";

            entry.target.style.transform = "translateY(0)";

        }

    });

}, {

    threshold: 0.2

});

images.forEach(img => {

    img.style.opacity = "0";

    img.style.transform = "translateY(40px)";

    img.style.transition = ".8s";

    imageObserver.observe(img);

});


// ==========================
// Loading Animation
// ==========================

window.addEventListener("load", () => {

    document.body.style.opacity = "1";

});


// ==========================
// Console Message
// ==========================

console.log(
`
========================================
 VEERA VAANJI MARTIAL ARTS ACADEMY
 Website Developed Successfully
========================================
`
);