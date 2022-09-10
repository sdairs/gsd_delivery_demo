<script lang="ts">
	import { Column, Row } from 'carbon-components-svelte';
	import ParcelTrackerForm from '$lib/components/ParcelTrackerForm.svelte';
	import ParcelTrackerTable from '$lib/components/ParcelTrackerTable.svelte';

	let order_id: string | number | null;

	function submit_callback() {
		get_parcel(order_id);
	}

	let parcel_search: boolean = false;
	let loading: boolean = false;
	let parcel_data: object = {};
	async function get_parcel(order_id) {
		loading = true;
		parcel_search = true;

		let params: URLSearchParams = new URLSearchParams({ order_id: order_id, type: 'history' });
		let url: URL = new URL('https://api.tinybird.co/v0/pipes/track_parcel_journey_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJiM2IxYTllZi04OTZlLTQxZTktYmRjMS01YzBkOWU5Njc5MDYifQ.fnPNj4_8PMMa7QuFx53tQBKmsmcBIIWcXG0ChDiKyJ0'
			}
		}).then((r) => r.json());

		parcel_data = result['data'][0];
		loading = false;
	}
</script>

{#if !parcel_search}
	<Row>
		<Column lg={{ span: 4, offset: 6 }}>
			<h1>Parcel Tracker</h1>
			<ParcelTrackerForm on:click={submit_callback} bind:order_id />
		</Column>
	</Row>
{:else if parcel_search && !loading}
	<Row>
		<Column lg={{ span: 4, offset: 6 }}>
			<h1>Parcel Tracker</h1>
			<ParcelTrackerTable {parcel_data} />
		</Column>
	</Row>
{/if}

<style>
	h1 {
		text-align: center;
		padding-bottom: 1rem;
	}
</style>
