let currentSort = {
    column: null,
    direction: 'asc' // 'asc' or 'desc'
};

function sortTable(column) {
    let table = document.getElementById('product-list');
    let rows = Array.from(table.getElementsByTagName('li'));
    
    // Exclude the last row (Jami row) from the sorting
    let rowsToSort = rows.slice(0, rows.length - 1);

    let index;
    switch (column) {
        case 'number': index = 0; break;
        case 'quantity': index = 3; break;
        case 'price': index = 4; break;
        case 'total': index = 5; break;
        case 'difference': index = 8; break;
    }

    // Toggle the direction
    if (currentSort.column === column) {
        currentSort.direction = (currentSort.direction === 'asc') ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    // Sort the rows based on the column
    rowsToSort.sort((a, b) => {
        let aText = a.getElementsByTagName('div')[index].textContent.trim();
        let bText = b.getElementsByTagName('div')[index].textContent.trim();

        // Handle sorting for different types of columns
        if (column === 'number') {
            // Sort numerically by number
            aText = parseInt(aText, 10);
            bText = parseInt(bText, 10);
        } else if (column === 'quantity' || column === 'difference') {
            // Extract the numeric part from quantity and difference (e.g., '1 ta' or '15 kun')
            aText = parseInt(aText.split(' ')[0], 10);
            bText = parseInt(bText.split(' ')[0], 10);
        } else if (column === 'price' || column === 'total') {
            // Sort numerically for price and total
            aText = parseFloat(aText.replace('$', '').trim());
            bText = parseFloat(bText.replace('$', '').trim());
        }

        if (currentSort.direction === 'asc') {
            return aText > bText ? 1 : (aText < bText ? -1 : 0);
        } else {
            return aText < bText ? 1 : (aText > bText ? -1 : 0);
        }
    });

    // Reorder the rows in the correct order
    rowsToSort.forEach(row => table.appendChild(row));

    // Append the last row (the Jami row) back at the end
    let jamiRow = rows[rows.length - 1];
    table.appendChild(jamiRow);

    // Update icons
    updateIcons(column);
}

function updateIcons(column) {
    // Reset all icons
    ['number', 'quantity', 'price', 'total', 'difference'].forEach(c => {
        let icon = document.getElementById(c + '-icon');
        icon.classList.remove('icon-up', 'icon-down');
    });

    // Set the icon for the selected column
    let icon = document.getElementById(column + '-icon');
    if (currentSort.direction === 'asc') {
        icon.classList.add('icon-up');
    } else {
        icon.classList.add('icon-down');
    }
}
