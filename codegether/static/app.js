// const showdown = window.showdown

const converter = new showdown.Converter();

const markdownElements = {
    // HEADINGS
    h1: " text-3xl font-bold my-3",
    h2: " text-2xl font-semibold my-3",
    h3: " text-xl font-semibold my-2",
    h4: " text-lg font-semibold",
    h5: " font-semibold",
    h6: " text-sm font-semibold",

    // LINK
    a: " text-blue-600 visited:text-purple-800 hover:underline",

    // LISTS
    ul: " list-disc",
    ol: " list-decimal",
    li: " my-1 ml-8",

    // OTHERS
    blockquote: " border-l-4 p-1 pl-5 my-2 bg-gray-100",
    pre: " border rounded p-3 my-2",
    img: " m-5",
};

const readTitle = (id_source, id_display, empty_message) => {
    const source = document.getElementById(id_source);
    const display = document.getElementById(id_display);

    if (!source.value)
        display.innerHTML = `<h1 class="text-3xl text-gray-400 mb-5">${empty_message}</h1>`;
    else
        display.innerHTML = `<h1 class="text-3xl font-bold mb-5">${source.value}</h1>`;

    MathJax.Hub.Queue(["Typeset", MathJax.Hub, id_display]);
};

const readMarkdown = (id_source, id_display, empty_message) => {
    const source = document.getElementById(id_source);
    const display = document.getElementById(id_display);

    if (!source.value)
        display.innerHTML = `<p class="text-gray-400">${empty_message}</p>`;
    else {
        display.innerHTML = converter.makeHtml(source.value.replace(/_/g, "ÿ"));
    }

    display.innerHTML = display.innerHTML.replace(/ÿ/g, "_");
    reloadMarkdown(id_display);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, id_display]);
};

const reloadMarkdown = (id) => {
    const div = document.getElementById(id);
    for (const tag in markdownElements) {
        const elementList = div.getElementsByTagName(tag);
        for (let i = 0; i < elementList.length; i++)
            elementList[i].className += markdownElements[tag];
    }
};
