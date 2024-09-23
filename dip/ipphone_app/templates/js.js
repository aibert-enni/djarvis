const employersData = JSON.parse('{{ all_employers_json|escapejs }}');
const allDepartments = JSON.parse('{{ departments_json|escapejs }}');
const searchInput = document.getElementById('search_here');
const tableBody = document.getElementById('table-body');
const isAdminInput = document.getElementById('is-admin');
const isAdmin = isAdminInput ? isAdminInput.value === 'true' : false;

searchInput.addEventListener('keyup', (e) => {
	const searchValue = e.target.value.toLowerCase();
	
	// Фильтрация данных по всем полям
	const filteredEmployers = employersData.filter(employer => {
		return Object.values(employer).some(value =>
			String(value).toLowerCase().includes(searchValue)
		);
	});

	// Очистка таблицы
	tableBody.innerHTML = "";

	// Группировка сотрудников по департаментам
	const departmentsMap = {};

	filteredEmployers.forEach(employer => {
		const departmentName = employer.department__name;

		
		if (!departmentsMap[departmentName]) {
			departmentsMap[departmentName] = [];
		}
		departmentsMap[departmentName].push(employer);
	});
	
	// Вывод департаментов и сотрудников
	Object.keys(departmentsMap).forEach(departmentName => {
		const department = allDepartments.find(dept => dept.name === departmentName);
		if (isAdmin && (departmentName === "null" || departmentsMap[departmentName].every(employer => !employer.is_active))) {
			// Департамент без сотрудников вообще (только для админа)
			const departmentRow = `
				<tr class="default-department department-row">
					<td colspan="5" class="text-left department"><strong>Неактивные пользователи и пользователи без департамента</strong></td>
				</tr>
			`;
			tableBody.innerHTML += departmentRow;

			filteredEmployers.forEach(employer => {
				// Проверка на сотрудников без департамента или неактивных сотрудников
				if (!employer.department__name || employer.department__name.trim() === "" || !employer.is_active) {
					const row = `
						<tr data-record="${employer.id}" onclick="openEditRecordModal('${employer.is_active}', '${employer.id}', '${employer.full_name}', '${employer.position}', '${employer.position_id}', '${employer.phone}', '${employer.email}', '${employer.room}')">
							<td>${employer.phone}</td>
							<td>${employer.full_name}</td>
							<td>${employer.position}</td>
							<td>${employer.room}</td>
							<td>${employer.email}</td>
						</tr>
					`;
					tableBody.innerHTML += row;
				}
			});
		} else if (departmentName !== "null") {
			const departmentRow = `
				<tr class="department-row department" onclick="openEditDepartmentModal('${department.id}', '${department.name}', '${department.position}')">
					<td colspan="5" class="text-left department"><strong>${departmentName}</strong></td>
				</tr>
			`;
			tableBody.innerHTML += departmentRow;

			departmentsMap[departmentName].forEach(employer => {
				if (employer.is_active) {
					const row = `
						<tr data-record="${employer.id}" data-department="${employer.department__name}" onclick="openEditRecordModal('${employer.is_active}', '${employer.id}', '${employer.full_name}', '${employer.position}', '${employer.position_id}', '${employer.phone}', '${employer.email}', '${employer.room}')">
							<td>${employer.phone}</td>
							<td>${employer.full_name}</td>
							<td>${employer.position}</td>
							<td>${employer.room}</td>
							<td>${employer.email}</td>
						</tr>
					`;
					tableBody.innerHTML += row;
				}
			});
		}
	});

	// Если ничего не найдено
	if (filteredEmployers.length === 0) {
		tableBody.innerHTML = `
			<tr>
				<td colspan="5">По запросу ничего не найдено...</td>
			</tr>
		`;
	}
});