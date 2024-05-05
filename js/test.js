// const colorPalette = [
//     'dodgetblue',
//     'crimson',
//     'gold',
//     'lawngreen',
//     'orange',
//     'blueviolet'
// ];
const colorPalette = [
    '#1a29d6',
    '#b7fbb1',
    '#FCF6A1',
    '#F08B32',
    '#82122C',
    '#572e7e'
];
function getRandomColor() {
    const randomIndex = Math.floor(Math.random() * colorPalette.length);
    return colorPalette[randomIndex];
}

document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.homeBar a');
    
    links.forEach(function (link) {
        link.addEventListener('mouseover', function () {
            link.style.color = getRandomColor();
        });

        link.addEventListener('mouseout', function () {
            link.style.color = '';
        });
    });
});