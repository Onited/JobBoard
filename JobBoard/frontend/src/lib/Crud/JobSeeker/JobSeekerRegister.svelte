<script>
	import '../../../app.css';

	const registerData = {
		firstname: '',
		lastname: '',
		email: '',
		phone: null,
		city: null,
		password: '',
		image_profile: null,
		genre: '',
		birthdate: null,
		cv: null,
	};

	async function register() {

		const response = await fetch('http://127.0.0.1:8000/jobSeeker/create', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(registerData)
		});

		if (response.ok) {
			// rediriger l'utilisateur vers la page de login :
			window.location.href = '/jslogin';
		} else {
			console.error('Registration failed:', await response.json());
			console.error('Error details:', response);
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center">
	<div class="rounded-lg shadow-md bg-rich-black form-width form-padding">
		<h2 class="text-4xl font-bold mb-6 underline titre col-baby-powder text-center">Register</h2>

		<form>
			<div class="mb-4 label-input-width block mx-auto">
				<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
					>First Name :
					<input
						bind:value={registerData.firstname}
						class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
						type="text"
						placeholder="Example: John"
						required
					/>
				</label>
			</div>

			<div class="mb-4 label-input-width block mx-auto">
				<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
					>Last Name :
					<input
						type="text"
						bind:value={registerData.lastname}
						class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
						placeholder="Example: Doe"
						required
					/>
				</label>
			</div>

			<div class="mb-4 label-input-width block mx-auto">
				<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
					>Email :
					<input
						type="email"
						bind:value={registerData.email}
						class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
						placeholder="Example@gmail.com"
						required
					/>
				</label>
			</div>

			<div class="mb-4 label-input-width block mx-auto">
				<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
					>Password :
					<input
						type="password"
						bind:value={registerData.password}
						class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
						placeholder="Password"
						required
					/>
				</label>
			</div>

			<div class="mb-4 label-input-width block mx-auto">
				<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
					>Genre :
					<select
						bind:value={registerData.genre}
						class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
						required
					>
						<option value="" disabled selected>Select Gender</option>
						<option value="male">Male</option>
						<option value="female">Female</option>
						<option value="other">Other</option>
					</select></label
				>
			</div>

			<button
				class="block mx-auto w-32 text-xl bg-indigo-dye bg-indigo-dye-darker py-1 rounded-xl sous-titre col-baby-powder mt-6"
				on:click={register}>Register</button
			>
		</form>

		<p class="mt-4 text-sm col-baby-powder text-center">
			You already have an account ?<br />
			<a href="/jslogin" class="underline">Sign In here</a> !
		</p>
	</div>
</div>
