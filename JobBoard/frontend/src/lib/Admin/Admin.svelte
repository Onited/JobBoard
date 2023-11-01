<script lang="ts">
	import { getJobSeekers, deleteJobSeeker, getCompanies, deleteCompany } from '$lib/api';
	import { goto } from '$app/navigation';

	let jobSeekers: any[] = [];
	let selectedJobSeekerId: any = null;
	let company: any[] = [];
	let selectedCompanyId: any = null;

	getJobSeekers().then((response) => {
		jobSeekers = response.data;
	});

	async function handleDelete() {
		if (selectedJobSeekerId) {
			await deleteJobSeeker(selectedJobSeekerId);
		}
	}

	async function handleUpdate() {
		if (selectedJobSeekerId) {
			await goto(`admin/jobseeker/update/${selectedJobSeekerId}`);
		}
	}

	async function handleCreate() {
		await goto('admin/jobseeker/create');
	}

	getCompanies().then((response) => {
		company = response.data;
	});

	async function handleCompanyDelete() {
		if (selectedCompanyId) {
			await deleteCompany(selectedCompanyId);
		}
	}

	async function handleCompanyUpdate() {
		if (selectedCompanyId) {
			await goto(`admin/company/update/${selectedCompanyId}`);
		}
	}

	async function handleCompanyCreate() {
		await goto('admin/company/create');
	}
</script>

<div>
	<div>
		<h2>Job Seekers</h2>

		<div>
			<label>
				<select bind:value={selectedJobSeekerId}>
					{#each jobSeekers as jobSeeker}
						<option value={jobSeeker.jobSeeker_id}>
							{jobSeeker.firstname}
							{jobSeeker.lastname} | {jobSeeker.email}
						</option>
					{/each}
				</select>
				<button on:click={handleDelete}>Delete</button>
				<button on:click={handleUpdate}>Update</button>
			</label>
		</div>

		<button on:click={handleCreate}>Create a JobSeeker</button>
	</div>

	<div>
		<h2>Companies</h2>

		<div>
			<label>
				<select bind:value={selectedCompanyId}>
					{#each company as company}
						<option value={company.company_id}>
							{company.company_name} | {company.email}
						</option>
					{/each}
				</select>
				<button on:click={handleCompanyDelete}>Delete</button>
				<button on:click={handleCompanyUpdate}>Update</button>
			</label>
		</div>

		<button on:click={handleCompanyCreate}>Create a Company</button>
	</div>
</div>
