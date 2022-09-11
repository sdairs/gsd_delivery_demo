<script lang="ts">
	import { Column, Row } from 'carbon-components-svelte';
	import ParcelTrackerForm from '$lib/components/ParcelTrackerForm.svelte';
	import ParcelTrackerTable from '$lib/components/ParcelTrackerTable.svelte';
	import Metric from '$lib/components/dashboard/Metric.svelte';
	import SearchError from '$lib/components/SearchError.svelte';

	let order_id: string | number | null;
	let status: string;

	$: if (!parcel_data) {
		status = 'Awaiting Collection';
	} else if (parcel_data['time_at_depot'] == null) {
		status = 'Collected';
	} else if (parcel_data['time_with_driver'] == null) {
		status = 'At Depot';
	} else if (parcel_data['time_delivered'] == null) {
		status = 'Out For Delivery';
	} else {
		status = 'Delivered';
	}

	function submit_callback() {
		get_parcel(order_id);
	}

	let parcel_search: boolean = false;
	let loading: boolean = false;
	let parcel_data: object = {};
	let search_error = false;

	async function get_order_event(order_id) {

	}

	async function get_parcel(order_id) {
		loading = true;
		parcel_search = true;

		let params: URLSearchParams = new URLSearchParams({ order_id: order_id, type: 'history' });
		let url: URL = new URL(
			'https://api.tinybird.co/v0/pipes/track_parcel_journey_by_id.json?' + params
		);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJiM2IxYTllZi04OTZlLTQxZTktYmRjMS01YzBkOWU5Njc5MDYifQ.fnPNj4_8PMMa7QuFx53tQBKmsmcBIIWcXG0ChDiKyJ0'
			}
		}).then((r) => r.json());

		if (result['data'].length > 0) {
			parcel_data = result['data'][0];
			get_driver_name(parcel_data['driver_id']);
			loading = false;
			search_error = false;
		} else {
			parcel_data = {};
			parcel_search = false;
			loading = false;
			search_error = true;
		}
	}

	async function get_driver_name(driver_id: string) {
		let params: URLSearchParams = new URLSearchParams({ driver_id: driver_id });
		let url = new URL('https://api.tinybird.co/v0/pipes/get_driver_name_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJiYmYwOTAzMy03ODAzLTQ4M2YtODNmMi1iOGQ5N2Q0NzBiNDMifQ.kdShMAz3fwT2jrge3ZDYN3ft02qKlipUpt2_nqrpWFI'
			}
		}).then((r) => r.json());

		parcel_data['driver_id'] = result['data'][0]['name'];
	}
</script>

{#if !parcel_search}
	<Row>
		<Column lg={{ span: 4, offset: 6 }}>
			<h1>Parcel Tracker</h1>
			{#if search_error}
				<SearchError error_message={'ID Not Found'} />
			{/if}
			<ParcelTrackerForm on:click={submit_callback} bind:order_id />
		</Column>
	</Row>
{:else if parcel_search && !loading}
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<h1>Parcel Tracker</h1>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<Metric metric={status} title={'Parcel Status'} />
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<ParcelTrackerTable {parcel_data} {order_id} />
		</Column>
	</Row>
{/if}

<style>
	h1 {
		text-align: center;
		padding-bottom: 1rem;
	}
</style>
