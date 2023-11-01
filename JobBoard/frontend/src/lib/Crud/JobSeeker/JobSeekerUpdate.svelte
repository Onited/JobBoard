<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	const jobSeekerId = $page.params.jobSeekerId;

	let fields: any = {};

	const updateData = {
		firstname: null,
		lastname: null,
		email: null,
		phone: null,
		city: null,
		password: null,
		image_profile: null,
		genre: null,
		birthdate: null,
		cv: null
	};

	async function getJobSeeker() {
		const url = `http://127.0.0.1:8000/jobSeeker/id/${encodeURIComponent(jobSeekerId)}`;
		const response = await fetch(url, {
			method: 'GET',
			headers: {
				accept: 'application/json'
			}
		});

		if (response.ok) {
			fields = await response.json();
		} else {
			console.error('Get all fields failed:', await response.text());
		}
	}

	async function updateJobSeeker() {
		const url = `http://127.0.0.1:8000/jobSeeker/update/${encodeURIComponent(jobSeekerId)}`;
		const response = await fetch(url, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(updateData)
		});

		if (response.ok) {
			goto('/admin');
		} else {
			console.error('Registration failed:', await response.json());
			console.error('Error details:', response);
		}
	}

	onMount(() => {
		getJobSeeker();
	});
</script>

{#if Object.keys(fields).length > 0}
	<div>
		<p>Firstname :</p>
		<input type="text" placeholder={fields.firstname} bind:value={updateData.firstname} />
		<br />
		<p>Lastname :</p>
		<input type="text" placeholder={fields.lastname} bind:value={updateData.lastname} />
		<br />
		<p>Email :</p>
		<input type="email" placeholder={fields.email} bind:value={updateData.email} />
		<br />
		<p>Phone :</p>
		<input type="tel" placeholder={fields.phone} bind:value={updateData.phone} />
		<br />
		<p>City :</p>
		<input type="text" placeholder={fields.city} bind:value={updateData.city} />
		<br />
		<p>Password :</p>
		<input type="password" bind:value={updateData.password} />
		<br />
		<p>Image Profile :</p>
		<input type="url" placeholder={fields.image_profile} bind:value={updateData.image_profile} />
		<br />
		<p>Genre :</p>
		<select bind:value={updateData.genre}>
			<option value={fields.genre} disabled selected>{fields.genre}</option>
			<option value="male">Male</option>
			<option value="female">Female</option>
			<option value="other">Other</option>
		</select>
		<br />
		<p>Birthdate :</p>
		<input type="datetime" placeholder={fields.birthdate} bind:value={updateData.birthdate} />
		<br />
		<p>CV :</p>
		<input type="url" placeholder={fields.cv} bind:value={updateData.cv} />
		<br />
		<button on:click={updateJobSeeker}>Update</button>
	</div>
{:else}
	<p>Loading...</p>
{/if}
