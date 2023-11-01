<script>
	import { goto } from "$app/navigation";

	const fields = {
		firstname: 'string',
		lastname: 'string',
		email: 'string',
		phone: null,
		city: null,
		password: 'string',
		image_profile: null,
		genre: 'string',
		birthdate: null,
		cv: null,
	};

	async function register() {

		const response = await fetch('http://127.0.0.1:8000/jobSeeker/create', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(fields)
		});

		if (response.ok) {
			goto('/admin');
		} else {
			console.error('Registration failed:', await response.json());
			console.error('Error details:', response);
		}
	}
</script>

		<div>
			<p>Firstname :</p>
			<input type="text" placeholder={fields.firstname} bind:value={fields.firstname} />
			<br />
			<p>Lastname :</p>
			<input type="text" placeholder={fields.lastname} bind:value={fields.lastname} />
			<br />
			<p>Email :</p>
			<input type="email" placeholder={fields.email} bind:value={fields.email} />
			<br />
			<p>Phone :</p>
			<input type="tel" placeholder={fields.phone} bind:value={fields.phone} />
			<br />
			<p>City :</p>
			<input type="text" placeholder={fields.city} bind:value={fields.city} />
			<br />
			<p>Password :</p>
			<input type="password" bind:value={fields.password} />
			<br />
			<p>Image Profile :</p>
			<input type="url" placeholder={fields.image_profile} bind:value={fields.image_profile} />
			<br />
			<p>Genre :</p>
			<select bind:value={fields.genre}>
				<option value={fields.genre} disabled selected>{fields.genre}</option>
				<option value="male">Male</option>
				<option value="female">Female</option>
				<option value="other">Other</option>
			</select>
			<br />
			<p>Birthdate :</p>
			<input type="datetime" placeholder={fields.birthdate} bind:value={fields.birthdate} />
			<br />
			<p>CV :</p>
			<input type="url" placeholder={fields.cv} bind:value={fields.cv} />
			<br />
			<button on:click={register}>Create a JobSeeker</button>
		</div>
