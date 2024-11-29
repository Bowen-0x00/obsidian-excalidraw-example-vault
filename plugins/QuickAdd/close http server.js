module.exports = async (params) => {
    const {
        quickAddApi: { inputPrompt },
        app,
    } = params;
    fetch('http://127.0.0.1:3456/close', {
        method: 'GET',
        mode: 'no-cors',
        headers: {
            'Origin': 'app://obsidian.md'
        }
    });
}