window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.getElementById("loader").style.top = '-100vh';
    }, 1000);

    const inputs = document.querySelectorAll("input:not([type='submit']), textarea");

    inputs.forEach(input => {
        input.addEventListener("focus", function () {
            inputs.forEach(i => {
                i.style.borderBottom = "2px solid #db0c4a";
            });
            this.style.borderBottom = "2px solid black";
        });
    });
});
