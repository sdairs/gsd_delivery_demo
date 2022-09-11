<script lang="ts">
	import Metric from '$lib/components/dashboard/Metric.svelte';
	import ParcelOrderTable from '$lib/components/ParcelOrderTable.svelte';
	import ParcelTrackerForm from '$lib/components/ParcelTrackerForm.svelte';
	import ParcelTrackerTable from '$lib/components/ParcelTrackerTable.svelte';
	import SearchError from '$lib/components/SearchError.svelte';
	import { Row, Column } from 'carbon-components-svelte';
	import { onMount } from 'svelte';

	let token: string | null;
	onMount(() => {
		token = new URL(document.location).searchParams.get('token');
	});

	let order_id: string;
	let order_event: object = {};
	let search_active: boolean = false;
	let order_search_loading: boolean = false;
	let journey_search_loading: boolean = false;
	let search_error: boolean = false;
	let parcel_journey: object = {};
	let parcel_status: string;
	$: if (search_error == true) {
		order_id = '';
		order_search_loading = false;
		journey_search_loading = false;
		search_active = false;
	}
	$: if (!parcel_journey || Object.keys(parcel_journey).length == 0) {
		parcel_status = 'Awaiting Collection';
	} else if (parcel_journey['time_at_depot'] == null) {
		parcel_status = 'Collected';
	} else if (parcel_journey['time_with_driver'] == null) {
		parcel_status = 'At Depot';
	} else if (parcel_journey['time_delivered'] == null) {
		parcel_status = 'Out For Delivery';
	} else {
		parcel_status = 'Delivered';
	}

	async function get_order_event_by_id(order_id: string) {
		order_search_loading = true;
		const params = new URLSearchParams({ order_id: order_id });
		const url = new URL('https://api.tinybird.co/v0/pipes/get_order_event_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICIyOWNjNzQzMS00OGNkLTRhN2EtYjZjYy0yOTIwYTA5YjdiMDEifQ.cbPn9-WIMi-xNlGCqa12UNoLvvpnICKkHuDXHFP_z1w'
			}
		})
			.then((r) => r.json())
			.then((r) => r);

		if (result['data'].length > 0) {
			// Order Found
			order_event = result['data'][0];
			search_error = false;
			order_search_loading = false;
		} else {
			// Order Not Found
			search_error = true;
		}
	}

	async function track_parcel_journey_by_id(order_id: string) {
		journey_search_loading = true;
		const params = new URLSearchParams({ order_id: order_id });
		let url = new URL('https://api.tinybird.co/v0/pipes/track_parcel_journey_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJiM2IxYTllZi04OTZlLTQxZTktYmRjMS01YzBkOWU5Njc5MDYifQ.fnPNj4_8PMMa7QuFx53tQBKmsmcBIIWcXG0ChDiKyJ0'
			}
		}).then((r) => r.json());
		if (result['data'].length > 0) {
			// Journey Found
			parcel_journey = result['data'][0];
			journey_search_loading = false;
		} else {
			// Journey Not Found
			journey_search_loading = false;
		}
	}

	function search() {
		search_active = true;
		get_order_event_by_id(order_id);
		track_parcel_journey_by_id(order_id);
	}
</script>

<Row>
	<Column lg={{ span: 4, offset: 6 }}>
		<h1>Parcel Tracker</h1>
	</Column>
</Row>
{#if search_error}
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<SearchError error_message={'No Order Found'} />
		</Column>
	</Row>
{/if}
{#if !search_active}
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<ParcelTrackerForm on:click={search} bind:order_id />
		</Column>
	</Row>
{/if}
{#if search_active && !journey_search_loading && !order_search_loading}
	<Row padding>
		<Column lg={{ span: 4, offset: 6 }}>
			<Metric metric={parcel_status} title={'Parcel Status'} />
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 10, offset: 3 }}>
			<h3>Order Details</h3>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 10, offset: 3 }}>
			<ParcelOrderTable order_data={order_event} />
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 10, offset: 3 }}>
			<h3>Journey Details</h3>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 10, offset: 3 }}>
			<ParcelTrackerTable
				parcel_data={parcel_journey}
				order_id={order_event['order_id']}
				order_time={order_event['time_ordered']}
			/>
		</Column>
	</Row>
{/if}

<style>
	h1 {
		text-align: center;
	}
</style>
