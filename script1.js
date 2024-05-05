function getHeaderHeight(){
    const header = document.querySelector('header');
    const headerHeight = header.offsetHeight;
    window.headerHeight = headerHeight;
    return headerHeight;
}

getHeaderHeight();


