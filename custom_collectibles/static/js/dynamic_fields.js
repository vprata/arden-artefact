document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('customFieldsContainer');
    const addBtn = document.getElementById('addFieldBtn');
    if (!container || !addBtn) return;

    let fieldIndex = container.querySelectorAll('.field-row').length;

    function applyValueInput(selectEl) {
        const row = selectEl.closest('.field-row');
        if (!row) return;
        const valueWrap = row.querySelector('.field-value-wrap');
        if (!valueWrap) return;
        const current = valueWrap.querySelector('[name^="field_value_"]');
        const name = current ? current.getAttribute('name') : null;
        const existing = current ? current.value : '';
        const type = selectEl.value;

        let html = '';
        if (type === 'number') {
            html = '<input type="number" step="any" name="' + name + '" class="form-control" placeholder="Number" value="' + existing + '" required>';
        } else if (type === 'date') {
            html = '<input type="date" name="' + name + '" class="form-control" value="' + existing + '" required>';
        } else if (type === 'boolean') {
            const yes = (existing === 'True' || existing === 'true' || existing === 'Yes' || existing === '1') ? 'selected' : '';
            const no = (existing === 'False' || existing === 'false' || existing === 'No' || existing === '0') ? 'selected' : '';
            html = '<select name="' + name + '" class="form-select" required>' +
                   '<option value="">Select…</option>' +
                   '<option value="true" ' + yes + '>Yes</option>' +
                   '<option value="false" ' + no + '>No</option>' +
                   '</select>';
        } else {
            html = '<input type="text" name="' + name + '" class="form-control" placeholder="Value" value="' + existing + '">';
        }
        valueWrap.innerHTML = html;
    }

    addBtn.addEventListener('click', function () {
        const row = document.createElement('div');
        row.className = 'row g-2 mb-2 field-row';
        row.innerHTML =
            '<div class="col-md-4">' +
            '<input type="text" name="field_name_' + fieldIndex + '" class="form-control" placeholder="Field name" required>' +
            '</div>' +
            '<div class="col-md-3">' +
            '<select name="field_type_' + fieldIndex + '" class="form-select field-type-select">' +
            '<option value="text">Text</option>' +
            '<option value="number">Number</option>' +
            '<option value="date">Date</option>' +
            '<option value="boolean">Boolean</option>' +
            '</select>' +
            '</div>' +
            '<div class="col-md-4 field-value-wrap">' +
            '<input type="text" name="field_value_' + fieldIndex + '" class="form-control" placeholder="Value">' +
            '</div>' +
            '<div class="col-md-1">' +
            '<button type="button" class="btn btn-outline-danger btn-sm remove-field">×</button>' +
            '</div>';
        container.appendChild(row);
        fieldIndex++;
    });

    container.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-field')) {
            e.target.closest('.field-row').remove();
        }
    });

    container.addEventListener('change', function (e) {
        if (e.target.classList.contains('field-type-select')) {
            applyValueInput(e.target);
        }
    });

    container.querySelectorAll('.field-type-select').forEach(applyValueInput);
});
