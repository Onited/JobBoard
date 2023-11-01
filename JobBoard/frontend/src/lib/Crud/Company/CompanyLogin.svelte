<script>
	import '../../app.css';

	const loginData = {
		email: '',
		password: ''
	};

	async function login() {
		const url = `http://127.0.0.1:8000/company/auth/${encodeURIComponent(loginData.email)}/${encodeURIComponent(loginData.password)}`;
		const response = await fetch(url, {
			method: 'GET'
		});

		if (response.ok) {
			window.location.href = '/';
		} else {
			console.error('Login failed:', await response.text());
		}
	}
</script>

<div class="min-h-screen flex items-center justify-center">
	<div class="rounded-lg shadow-md bg-rich-black form-width form-padding">
		<h2 class="text-4xl font-bold mb-6 underline titre col-baby-powder text-center">Log In</h2>

		<div class="mb-4 label-input-width block mx-auto">
			<label class="block text-xl font-medium mb-2 sous-titre col-baby-powder underline"
				>Email :
				<input
					bind:value={loginData.email}
					class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
					type="text"
					placeholder="Example@gmail.com"
					required
				/>
			</label>
		</div>

		<div class="mb-4 label-input-width block mx-auto">
			<label class="text-xl font-medium mb-2 sous-titre col-baby-powder underline">
				Password :
				<input
					type="password"
					bind:value={loginData.password}
					class="w-64 text-sm px-3 py-2 rounded-xl transition mx-auto block"
					placeholder="Password"
					required
				/>
			</label>
		</div>

		<button
			class="block mx-auto w-32 text-xl bg-indigo-dye bg-indigo-dye-darker py-1 rounded-xl sous-titre col-baby-powder mt-6"
			on:click={login}>Submit</button
		>

		<p class="mt-4 text-sm col-baby-powder text-center">
			You don't have an account ?<br />
			<a href="/companyregister" class="underline">Sign Up</a> !
		</p>
	</div>
</div>
