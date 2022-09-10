<script lang="ts">
	import { Column, Row } from 'carbon-components-svelte';
	import ParcelTrackerForm from '$lib/components/ParcelTrackerForm.svelte';
	import ParcelTrackerTable from '$lib/components/ParcelTrackerTable.svelte';
	import ParcelOrderTable from '$lib/components/ParcelOrderTable.svelte';
	import Metric from '$lib/components/dashboard/Metric.svelte';

	let order_id: string | number | null;

	function submit_callback() {
		get_order_event(order_id);
		track_parcel(order_id);
	}

	let parcel_search: boolean = false;
	let loading: boolean = false;
	let parcel_data: object = {};
	let order_data: object = {};
	let customer_metrics: object = {
		order_count: 0,
		order_value: 0
	};

	async function get_customer_metrics(customer_name: string, type: string) {
		let params: URLSearchParams = new URLSearchParams({ type: type, customer_name: customer_name });

		let url = new URL('https://api.tinybird.co/v0/pipes/get_customer_metrics.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI2NTc1ZWJhMC03NjYzLTQ4N2YtOWU0YS05YWUwMzExYmZjNDQifQ.WGw2Bb0bKW0vSrkFXoFkP_wX-TzPH9j3Nhukj3vKsH8'
			}
		})
			.then((r) => r.json())
			.then((r) => r)
			.catch((e) => e.toString());
		customer_metrics[type] = result['data'][0]['total'];
	}

	async function get_order_event(order_id: string) {
		let params: URLSearchParams = new URLSearchParams({ order_id: order_id });
		let url = new URL('https://api.tinybird.co/v0/pipes/get_order_event_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICIyOWNjNzQzMS00OGNkLTRhN2EtYjZjYy0yOTIwYTA5YjdiMDEifQ.cbPn9-WIMi-xNlGCqa12UNoLvvpnICKkHuDXHFP_z1w'
			}
		})
			.then((r) => r.json())
			.then((r) => r)
			.catch((e) => e.toString());

		order_data = result['data'][0];
		get_customer_metrics(order_data['customer_name'], 'order_count');
		get_customer_metrics(order_data['customer_name'], 'order_value');
	}

	async function track_parcel(order_id: string) {
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

		parcel_data = result['data'][0];
		loading = false;
	}
</script>

<Row>
	<Column lg={{ span: 4, offset: 6 }}>
		<h1>Customer Service</h1>
	</Column>
</Row>
{#if !parcel_search}
	<Row>
		<Column lg={{ span: 6, offset: 5 }}>
			<ParcelTrackerForm on:click={submit_callback} bind:order_id />
		</Column>
	</Row>
{:else if parcel_search && !loading}
	<Row padding>
		<Column lg={{ span: 6, offset: 5 }}>
			<h2>Customer Stats</h2>
		</Column>
	</Row>
	<Row>
		<Column lg={{ span: 6, offset: 5 }}>
			<Row>
				<Column>
					<Metric title={'Total Orders'} metric={customer_metrics['order_count']} />
				</Column>
				<Column>
					<Metric prefix={'£'} title={'Total Revenue'} metric={customer_metrics['order_value']} />
				</Column>
			</Row>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 6, offset: 5 }}>
			<h2>Order Details</h2>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 6, offset: 5 }}>
			<ParcelOrderTable {order_data} />
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 6, offset: 5 }}>
			<h2>Journey Details</h2>
		</Column>
	</Row>
	<Row padding>
		<Column lg={{ span: 6, offset: 5 }}>
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
