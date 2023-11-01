<script lang="ts">
	import { onMount } from 'svelte';

	// @ts-ignore
	let ads: any[] = [];

	async function getAllAds() {
		const url = `http://127.0.0.1:8000/advertisement/all`;
		const response = await fetch(url, {
			method: 'GET',
			headers: {
				accept: 'application/json'
			}
		});

		if (response.ok) {
			ads = await response.json();
		} else {
			console.error('Get all ads failed:', await response.text());
		}
	}

	onMount(() => {
		getAllAds();
	});
</script>

{#each ads as ads}
	<div class="job-ad">
		<div class="job-title">{ads.title}</div>
		<div class="job-type">{ads.job_type}</div>
		<div class="job-description">{ads.ad_description}</div>
		<div class="job-company">{ads.company_name}</div>
		<button
			class="bg-sky-950 text-sky-400 border border-sky-400 border-b-4 font-medium overflow-hidden relative px-4 py-2 rounded-md hover:brightness-150 hover:border-t-4 hover:border-b active:opacity-75 outline-none duration-300 group"
		>
			<span
				class="bg-sky-400 shadow-sky-400 absolute -top-[150%] left-0 inline-flex w-80 h-[5px] rounded-md opacity-50 group-hover:top-[150%] duration-500 shadow-[0_0_10px_10px_rgba(0,0,0,0.3)]"
			/>
			Learn More
		</button>
	</div>
{/each}
