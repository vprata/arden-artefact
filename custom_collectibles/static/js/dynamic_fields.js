/**
 * Dynamic custom field builder for Custom Collectibles.
 * Allows Collection Owners to add/remove fields at runtime.
 */
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('customFieldsContainer');
    const addBtn = document.getElementById('addFieldBtn');
    if (!container || !addBtn) return;

    let fieldIndex = container.querySelectorAll('.field-row').length;

    addBtn.addEventListener('click', function () {
        const row = document.createElement('div');
        row.className = 'row g-2 mb-2 field-row';
        row.innerHTML = `
            <div class="col-md-4">
                <input type="text" name="field_name_${fieldIndex}" class="form-control"
                       placeholder="Field name" required>
            </div>
            <div class="col-md-3">
                <select name="field_type_${fieldIndex}" class="form-select">
                    <option value="text">Text</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                    <option value="boolean">Boolean</option>
                </select>
            </div>
            <div class="col-md-4">
                <input type="text" name="field_value_${fieldIndex}" class="form-control"
                       placeholder="Value">
            </div>
            <div class="col-md-1">
                <button type="button" class="btn btn-outline-danger btn-sm remove-field">×</button>
            </div>
        `;
        container.appendChild(row);
        fieldIndex++;
    });

    container.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-field')) {
            e.target.closest('.field-row').remove();
        }
    });
});
