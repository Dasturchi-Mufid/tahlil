let currentSortState = {
    column: null,
    direction: 'asc' // 'asc' or 'desc'
};

function sortTable(columnName) {
    let itemList = document.getElementById('item-list');
    let itemRows = Array.from(itemList.getElementsByTagName('li'));

    // Exclude the last row (Jami row) from sorting
    let rowsToSort = itemRows.slice(0, itemRows.length - 1);

    let columnIndex;
    switch (columnName) {
        case 'identifier': columnIndex = 0; break;
        case 'type': columnIndex = 1; break;
        case 'quantity': columnIndex = 2; break;
        case 'totalAmount': columnIndex = 3; break;
        case 'percent': columnIndex = 4; break;
    }

    // Toggle the sorting direction
    if (currentSortState.column === columnName) {
        currentSortState.direction = (currentSortState.direction === 'asc') ? 'desc' : 'asc';
    } else {
        currentSortState.column = columnName;
        currentSortState.direction = 'asc';
    }

    // Sort the rows based on the column selected
    rowsToSort.sort((a, b) => {
        let textA = a.getElementsByTagName('div')[columnIndex].textContent.trim();
        let textB = b.getElementsByTagName('div')[columnIndex].textContent.trim();

        // Handle sorting for different types of columns
        if (columnName === 'identifier') {
            // Sort numerically by ID
            textA = parseInt(textA, 10);
            textB = parseInt(textB, 10);
        } else if (columnName === 'quantity') {
            // Extract numeric part of the quantity (e.g., '1 ta')
            textA = parseInt(textA.split(' ')[0], 10);
            textB = parseInt(textB.split(' ')[0], 10);
        } else if (columnName === 'totalAmount') {
            // Sort numerically for totalAmount
            textA = parseFloat(textA.replace('$', '').trim());
            textB = parseFloat(textB.replace('$', '').trim());
        } else if (columnName === 'percent') {
            // Sort numerically for percentage
            textA = parseFloat(textA.replace('%', '').trim());
            textB = parseFloat(textB.replace('%', '').trim());
        }

        // Determine the sorting order based on current direction
        if (currentSortState.direction === 'asc') {
            return textA > textB ? 1 : (textA < textB ? -1 : 0);
        } else {
            return textA < textB ? 1 : (textA > textB ? -1 : 0);
        }
    });

    // Reorder the rows in the correct order
    rowsToSort.forEach(row => itemList.appendChild(row));

    // Append the last row (the Jami row) back at the end
    let jamiRow = itemRows[itemRows.length - 1];
    itemList.appendChild(jamiRow);

    // Update sorting icons
    updateSortingIcons(columnName);
}

function updateSortingIcons(columnName) {
    // Reset all icons
    ['identifier', 'type', 'quantity', 'totalAmount', 'percent'].forEach(col => {
        let icon = document.getElementById(col + '-sort-icon');
        if (icon) {
            icon.classList.remove('icon-up', 'icon-down');
        }
    });

    // Set the icon for the selected column
    let icon = document.getElementById(columnName + '-sort-icon');
    if (icon) {
        if (currentSortState.direction === 'asc') {
            icon.classList.add('icon-up');
        } else {
            icon.classList.add('icon-down');
        }
    }
}
