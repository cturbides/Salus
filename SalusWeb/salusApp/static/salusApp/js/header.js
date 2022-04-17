class Header extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = `
        <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    header {        
        height: auto;
        padding: 48px;
        width: 100%;
    }

    .links a{
        display: inline-block;
        color: #fff;
        align-items: center;
        font-weight: 500;
        text-decoration: none;
        margin-top: 10px;
        border: 1px solid #fff;
        width: 150px;
        border-radius: 3px;
        text-align: center;
        padding: 10px 0px;
    }
    
    nav {
        box-sizing: border-box;
        display: flex;
        height: 20px;
        align-items: center;
        justify-content: space-between;
    }
    
    nav ul {
        list-style: none;
        padding: 0;
    }
    
    nav a {
        margin: 0px 25px;
        text-decoration: none;
        color: #fff;
        animation: moverIzquierda 1s ease-in;
    }
    
    img {
        display: inline-block;
        height: 100px;
        width: auto;
        object-fit: cover;
    }
</style>
<header>
    <nav>
        <a href="/Web/index.html" id="logo" class="logo"><img src="/Web/static/Logo_Salus.png"></a>
        <div class="links" id="links">
            <a href="">Home</a>
            <a href="/Web/common/login.html">Login</a>
        </div>
    </nav>
</header>
    `;
    }
}
customElements.define('header-component', Header)