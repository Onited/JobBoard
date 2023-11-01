import axios from 'axios';

const api = axios.create({
	baseURL: 'http://127.0.0.1:8000/jobSeeker',
});

const companyApi = axios.create({
	baseURL: 'http://127.0.0.1:8000/company',
});

// @ts-ignore
export async function getJobSeekers(data) {
	return api.get('/all', data);
}

// @ts-ignore
export async function createJobSeeker(data) {
	return api.post('/create', data);
}

// @ts-ignore
export async function updateJobSeeker(id, data) {
	return api.put(`/update/${id}`, data);
}

// @ts-ignore
export async function deleteJobSeeker(id) {
	return api.delete(`/delete/${id}`);
}

// @ts-ignore
export async function getCompanies(data) {
	return companyApi.get('/all', data);
}

// @ts-ignore
export async function createCompany(data) {
	return companyApi.post('/create', data);
}

// @ts-ignore
export async function updateCompany(id, data) {
	return companyApi.put(`/update/${id}`, data);
}

// @ts-ignore
export async function deleteCompany(id) {
	return companyApi.delete(`/delete/${id}`);
}
